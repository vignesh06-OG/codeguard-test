import os
from github import Github, Auth
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

def fetch_open_prs(repo_name: str) -> list[dict]:
    auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    prs = repo.get_pulls(state='open', sort='updated')

    result = []
    for pr in prs:
        files_data = []
        total_chars = 0
        MAX_CHARS = 80000

        for f in pr.get_files():
            if f.patch and total_chars < MAX_CHARS:
                chunk = f"### File: `{f.filename}`\n**Status:** {f.status}\n\n```diff\n{f.patch[:3000]}\n```\n"
                files_data.append(chunk)
                total_chars += len(chunk)

        result.append({
            "number": pr.number,
            "title": pr.title,
            "author": pr.user.login,
            "url": pr.html_url,
            "body": pr.body or "No description provided.",
            "diff": "\n".join(files_data),
            "pr_object": pr
        })

    return result


def post_review_to_github(pr_object, summary: str, risk_score: int):
    badge = "🔴" if risk_score >= 7 else "🟡" if risk_score >= 4 else "🟢"
    comment_body = f"## 🛡️ CodeGuard AI Review {badge}\n\n**Risk Score: {risk_score}/10**\n\n{summary}\n\n---\n*🤖 Automated review by CodeGuard AI — Powered by Gemini + CrewAI*"
    pr_object.create_issue_comment(comment_body)


def build_review_crew(pr_diff: str, pr_title: str):

    security_agent = Agent(
        role="Senior Application Security Engineer",
        goal="Find every exploitable security vulnerability in the code diff.",
        backstory="You are a battle-hardened AppSec engineer with 12 years of penetration testing experience. You think like an attacker. You know the OWASP Top 10 and CWE Top 25 by heart. You flag hardcoded secrets, injection flaws, auth issues, and insecure dependencies. You are methodical and paranoid by profession.",
        llm="gemini/gemini-2.5-flash",
        verbose=True,
        allow_delegation=False
    )

    quality_agent = Agent(
        role="Staff Software Engineer — Code Quality Specialist",
        goal="Identify logic bugs, performance issues, and code smell in the diff.",
        backstory="You are a pragmatic Staff Engineer who has reviewed thousands of PRs. You care about correctness, maintainability, and performance. You catch off-by-one errors, missing error handling, N+1 queries, memory leaks, and violations of DRY/SOLID principles. You do NOT re-flag security issues.",
        llm="gemini/gemini-2.5-flash",
        verbose=True,
        allow_delegation=False
    )

    synthesizer_agent = Agent(
        role="Engineering Manager — PR Review Synthesizer",
        goal="Synthesize all findings into a clear, structured, GitHub-ready review.",
        backstory="You are a senior engineering manager who writes PR reviews developers actually read and respect. You are direct but constructive. Your output is always clean GitHub Markdown.",
        llm="gemini/gemini-2.5-flash",
        verbose=True,
        allow_delegation=False
    )

    security_task = Task(
        description=f"""Analyze this PR titled "{pr_title}" for security vulnerabilities.

DIFF TO ANALYZE:
{pr_diff}

Check each category EXPLICITLY and report findings or CLEAN per category:
1. Injection Flaws (SQL, Command, LDAP, NoSQL)
2. Hardcoded Secrets / API Keys / Passwords
3. Broken Authentication or Missing Authorization checks
4. Sensitive Data Exposure (PII in logs, unencrypted storage)
5. Insecure Dependencies (suspicious imports)
6. Missing Input Validation / Sanitization
7. Insecure Deserialization

For each FINDING output:
- SEVERITY: [CRITICAL | HIGH | MEDIUM | LOW]
- FILE: filename
- LINE: approximate line number
- ISSUE: one sentence description
- EXPLOIT: how an attacker could use this
- FIX: corrected code snippet""",
        expected_output="Structured security findings with severity, file, line, issue, exploit, and fix for each vulnerability found.",
        agent=security_agent
    )

    quality_task = Task(
        description=f"""Analyze this PR titled "{pr_title}" for code quality issues.
Do NOT re-report security vulnerabilities.

DIFF TO ANALYZE:
{pr_diff}

Check for:
1. Logic bugs and off-by-one errors
2. Unhandled exceptions / missing try-catch
3. Functions over 25 lines (complexity smell)
4. Duplicate code (DRY violations)
5. Missing type hints or incorrect types
6. Performance anti-patterns (N+1 queries, blocking I/O, memory leaks)
7. Dead code or unused imports

For each FINDING output:
- TYPE: [BUG | PERFORMANCE | STYLE | COMPLEXITY]
- FILE: filename
- LINE: approximate line number
- ISSUE: one sentence description
- FIX: corrected code snippet""",
        expected_output="Structured quality findings with type, file, line, issue, and fix for each problem found.",
        agent=quality_agent
    )

    synthesis_task = Task(
        description="""Using the security and quality reports, write the final GitHub PR review.

Follow this EXACT markdown structure:

## Executive Summary
[2-3 sentence honest assessment]

## Risk Score: X/10
[One sentence justifying the score]

## 🔴 Must Fix Before Merge
[ONLY Critical and High items with FILE:LINE format]

## 🟡 Should Fix Soon
[Medium severity items]

## 🟢 Suggestions (Optional)
[Low severity items]

## Summary Table
| Severity | Count | Category |
|----------|-------|----------|
| 🔴 Critical | X | Security |
| 🟠 High | X | Security/Quality |
| 🟡 Medium | X | Quality |
| 🟢 Low | X | Style |

## Verdict
[APPROVE / REQUEST CHANGES / NEEDS DISCUSSION] — [one sentence reason]

Last line MUST be exactly:
RISK_SCORE:N""",
        expected_output="Complete GitHub-ready markdown review ending with RISK_SCORE:N on the last line.",
        agent=synthesizer_agent
    )

    crew = Crew(
        agents=[security_agent, quality_agent, synthesizer_agent],
        tasks=[security_task, quality_task, synthesis_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


def run_full_review(repo_name: str, post_to_github: bool = True):
    prs = fetch_open_prs(repo_name)

    if not prs:
        return []

    results = []
    for pr in prs:
        crew = build_review_crew(pr["diff"], pr["title"])
        raw_output = crew.kickoff()

        output_str = str(raw_output)
        risk_score = 5
        if "RISK_SCORE:" in output_str:
            try:
                score_part = output_str.split("RISK_SCORE:")[-1].strip()
                risk_score = int(''.join(filter(str.isdigit, score_part[:3])))
                risk_score = max(0, min(10, risk_score))
            except (ValueError, IndexError):
                pass

        if post_to_github:
            post_review_to_github(pr["pr_object"], output_str, risk_score)

        results.append({
            "pr_number": pr["number"],
            "pr_title": pr["title"],
            "pr_url": pr["url"],
            "author": pr["author"],
            "review": output_str,
            "risk_score": risk_score
        })

    return results