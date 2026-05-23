# 🛡️ CodeGuard AI — Autonomous PR Security Reviewer

## 🚨 Problem
Engineering teams merge vulnerable code daily without proper security review.
Manual code reviews are slow, inconsistent, and miss critical security flaws.

## ✅ Solution
A 3-agent AI system that autonomously reviews GitHub Pull Requests,
detects security vulnerabilities, and posts actionable review comments
directly on GitHub — automatically.

## 🏗️ Architecture
GitHub PR → Agent 1 (Security Auditor)
→ Agent 2 (Quality Analyst)
→ Agent 3 (Synthesizer)
→ GitHub Comment (Auto-posted)

## 🤖 How It Works
1. Fetches open Pull Requests from target GitHub repo
2. Agent 1 scans for OWASP Top 10 security vulnerabilities
3. Agent 2 checks code quality, bugs, and performance issues
4. Agent 3 synthesizes a structured review with Risk Score (0-10)
5. Review is automatically posted as a GitHub PR comment

## 🛠️ Tech Stack
- **CrewAI** — Multi-agent orchestration
- **Google Gemini 2.5 Flash** — LLM Brain
- **PyGithub** — GitHub API integration
- **Streamlit** — Live dashboard UI
- **LangChain** — LLM framework

## 🔍 What It Detects
- SQL Injection & Command Injection
- Hardcoded API Keys & Secrets
- Broken Authentication & IDOR
- Sensitive Data Exposure (PII in logs)
- Memory Leaks & Resource Management
- Missing Error Handling
- Performance Anti-patterns

## 🚀 Setup & Run
```bash
# 1. Clone the repo
git clone https://github.com/vignesh06-OG/codeguard-test

# 2. Create virtual environment
py -3.11 -m venv venv311
venv311\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
GEMINI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
GITHUB_REPO=owner/repo-name

# 5. Run
python -m streamlit run app.py
```

## 📊 Demo
> CodeGuard detected SQL Injection, Hardcoded API Keys & Memory Leaks
> in a test PR — Risk Score: 9/10 — Automatically posted on GitHub.

## 👥 Team
- **Vignesh** (Lead)
- **Sanzi**

- ## Our Contribution vs AI-Generated Output

### We Built (Human Contribution):
- Problem identification & solution design
- 3-agent architecture decision
- GitHub API integration logic
- Streamlit UI design & layout
- CrewAI orchestration & agent personas
- Security vulnerability categories defined
- Debugging & environment setup (Python 3.11 migration)
- End-to-end system integration & testing

### AI-Assisted (Tools Used):
- GitHub Copilot / Claude: Code suggestions & debugging help
- Google Gemini 2.5 Flash: LLM for actual code review
- CrewAI: Agent framework

## 🏆 Built For
AI Hackathon — May 2026
