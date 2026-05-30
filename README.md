# 🛡️ CodeGuard AI — Autonomous PR Security Reviewer

## 🚀 Live Demo
https://codeguard-test-production.up.railway.app

## 🚨 Problem
Engineering teams merge vulnerable code daily without proper security review.

## ✅ Solution
A 3-agent AI system that autonomously reviews GitHub Pull Requests,
detects security vulnerabilities, and posts actionable review comments
directly on GitHub — automatically.

## 🏗️ Architecture
GitHub PR → Agent 1 (Security Auditor) → Agent 2 (Quality Analyst) → Agent 3 (Synthesizer) → GitHub Comment

## 🛠️ Tech Stack
- **CrewAI** — Multi-agent orchestration
- **Google Gemini 2.5 Flash** — LLM Brain
- **PyGithub** — GitHub API integration
- **Streamlit** — Live dashboard UI

## 🔍 What It Detects
- SQL Injection & Command Injection
- Hardcoded API Keys & Secrets
- Broken Authentication & IDOR
- Memory Leaks & Resource Management
- Missing Error Handling

## 👥 Team
- **Vignesh** (Lead)
- **Sanzi**

## 🏆 Built For
AI Hackathon — May 2026
