# codeguard-test
# 🛡️ CodeGuard AI — Autonomous PR Security Reviewer

## Problem
Engineering teams merge vulnerable code daily without proper security review.

## Solution
A 3-agent AI system that autonomously reviews GitHub Pull Requests,
detects security vulnerabilities, and posts actionable comments directly on GitHub.

## Architecture
GitHub PR → Agent 1 (Security Auditor) → Agent 2 (Quality Analyst) 
→ Agent 3 (Synthesizer) → GitHub Comment

## Tech Stack
- CrewAI (Multi-agent orchestration)
- Google Gemini 2.5 Flash (LLM)
- PyGithub (GitHub API)
- Streamlit (Dashboard UI)

## What We Built
- 3-agent CrewAI system with specialized personas
- Real-time PR diff fetching and chunking
- Automated GitHub comment posting
- Risk scoring system (0-10)
- Live dashboard with token tracking

## Demo
[Video Link]

## Team
- Vignesh (Lead)
- Sanzi
