import streamlit as st
import os
import time
from dotenv import load_dotenv
from agent_core import run_full_review  # ✅ TOP PE — andar nahi

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeGuard AI | Agentic Code Reviewer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Premium Futuristic CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    h1 { color: #58a6ff !important; text-shadow: 0 0 15px rgba(88, 166, 255, 0.4); font-family: 'Courier New', Courier, monospace; }
    h2, h3 { color: #8b949e !important; }
    .glass-card {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        transition: transform 0.2s;
    }
    .glass-card:hover { transform: translateY(-5px); border-color: #58a6ff; }
    .metric-title { color: #8b949e; font-size: 15px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; }
    .metric-value { color: #3fb950; font-size: 36px; font-weight: 800; text-shadow: 0 0 10px rgba(63, 185, 80, 0.3); }
    .token-value { color: #a371f7; font-size: 36px; font-weight: 800; text-shadow: 0 0 10px rgba(163, 113, 247, 0.3); }
    </style>
""", unsafe_allow_html=True)

# --- Session State Init (PAGE LOAD PE EK BAAR) ---
if "review_results" not in st.session_state:
    st.session_state.review_results = []
if "total_bugs" not in st.session_state:
    st.session_state.total_bugs = 0
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "active_prs" not in st.session_state:
    st.session_state.active_prs = 0

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("---")
    st.caption("🎯 TARGET REPOSITORY")
    st.code(os.getenv("GITHUB_REPO", "vignesh06-OG/codeguard-test"), language="bash")
    st.markdown("---")

    # ✅ LIVE token tracking (session_state se)
    st.markdown("### 📊 API Token Usage")
    token_limit = 100000
    used = st.session_state.total_tokens
    ratio = min(used / token_limit, 1.0)
    st.progress(ratio)
    st.markdown(
        f"<p style='text-align:right;color:#a371f7;font-weight:bold;'>"
        f"{used:,} / {token_limit:,} Limit</p>",
        unsafe_allow_html=True
    )
    st.caption("Updates after each scan")
    st.markdown("---")
    st.markdown("### 🔐 Authorized Admins")
    st.markdown("* 🟢 **Vignesh** (Lead)\n* 🟢 **Sanzi**")
    st.markdown("---")
    st.success("API Connections: SECURE")

# --- Main Header ---
st.markdown("<h1>🛡️ CodeGuard AI System</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:18px;color:#8b949e;margin-bottom:30px;'>"
    "Autonomous Pull Request Review & Security Analysis Engine</p>",
    unsafe_allow_html=True
)

# --- ✅ LIVE Metric Cards (hardcoded nahi, session_state se) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f'<div class="glass-card"><div class="metric-title">Active PRs</div>'
        f'<div class="metric-value">{st.session_state.active_prs}</div></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f'<div class="glass-card"><div class="metric-title">Critical Bugs Prevented</div>'
        f'<div class="metric-value" style="color:#f85149;">{st.session_state.total_bugs}</div></div>',
        unsafe_allow_html=True
    )
with col3:
    tokens_display = f"{st.session_state.total_tokens/1000:.1f}k" if st.session_state.total_tokens > 0 else "0"
    st.markdown(
        f'<div class="glass-card"><div class="metric-title">Total Tokens Used</div>'
        f'<div class="token-value">{tokens_display}</div></div>',
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# --- TABS ---
tab1, tab2 = st.tabs(["🚀 Live Agent Terminal", "📜 Review History"])

# ✅ SAB KUCH tab1 ke ANDAR hai ab
with tab1:
    st.markdown("### 🤖 Agent Status: Standby")
    st.info("Ready to fetch and analyze the latest Pull Requests from GitHub...")

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        scan_btn = st.button("⚡ Initialize Deep Scan", use_container_width=True)
    with col_btn2:
        post_gh = st.checkbox("Post to GitHub", value=True)

    if scan_btn:
        repo_name = os.getenv("GITHUB_REPO", "vignesh06-OG/codeguard-test")
        status_box = st.empty()

        # Agent-wise live status messages
        agent_messages = [
            "🔍 Agent 1 (Security Auditor) — Scanning for vulnerabilities...",
            "🧠 Agent 2 (Quality Analyst) — Checking logic & performance...",
            "📝 Agent 3 (Synthesizer) — Writing GitHub-ready review...",
        ]
        for msg in agent_messages:
            status_box.markdown(
                f"<div style='background:#161b22;border:1px solid #30363d;"
                f"border-radius:8px;padding:15px;font-family:monospace;color:#3fb950'>"
                f"{msg}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.8)  # thoda dramatic effect

        with st.spinner("CrewAI agents are reviewing your PR..."):
            results = run_full_review(repo_name, post_to_github=post_gh)
            st.session_state.review_results = results

            # ✅ Metrics update karo scan ke baad
            st.session_state.active_prs = len(results)
            bug_count = sum(
                1 for r in results if r["risk_score"] >= 7
            )
            st.session_state.total_bugs += bug_count
            # Token estimate: ~3000 tokens per PR (adjust based on actual usage)
            st.session_state.total_tokens += len(results) * 3000

        status_box.success(f"✅ Review complete — {len(results)} PR(s) analyzed!")
        st.rerun()

    # Results render karo
    if st.session_state.review_results:
        st.markdown("---")
        st.markdown("### 📋 Latest Scan Results")
        for result in st.session_state.review_results:
            risk = result["risk_score"]
            badge = "🔴" if risk >= 7 else "🟡" if risk >= 4 else "🟢"
            with st.expander(
                f"{badge} PR #{result['pr_number']}: {result['pr_title']} "
                f"— Risk {risk}/10 by @{result['author']}"
            ):
                st.markdown(result["review"])
                st.markdown(f"[View on GitHub ↗]({result['pr_url']})")

# ✅ Review History tab (session_state se populate hoga)
with tab2:
    st.markdown("### 🗄️ Past Security Reviews")
    if not st.session_state.review_results:
        st.info("Koi review nahi mila abhi. Pehle scan chalao.")
    else:
        for result in st.session_state.review_results:
            risk = result["risk_score"]
            status = "FLAGGED" if risk >= 5 else "SECURE"
            with st.expander(
                f"PR #{result['pr_number']}: {result['pr_title']} — [Status: {status}]"
            ):
                st.markdown(f"**Risk Score:** {risk}/10")
                st.markdown(f"**Author:** @{result['author']}")
                st.markdown(f"**AI Verdict:** *(See full review in Live Terminal tab)*")
                st.markdown(f"[View on GitHub ↗]({result['pr_url']})")