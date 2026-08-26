import base64
from datetime import datetime
import streamlit as st

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Sentiment Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================
# SESSION STATE INITIALIZATION
# =====================================

if "user" not in st.session_state:
  st.session_state.user = {
      "name": "Monika Jangid",
      "username": "monika",
      "email": "monika@example.com",
      "role": "Data Analyst",
      "plan": "Premium",
      "bio": (
          "Final Year CSE Student · Aspiring Data Analyst · AI & NLP Enthusiast"
      ),
      "skills": ["Python", "SQL", "Power BI", "NLP"],
      "avatar_b64": None,
      "password_hash": "changeme",
  }

if "authenticated" not in st.session_state:
  st.session_state.authenticated = True

if "page" not in st.session_state:
  st.session_state.page = "Dashboard"

NAV_ITEMS = [
    ("Dashboard", "📊"),
    ("YouTube Analysis", "🎥"),
    ("News Analysis", "📰"),
    ("Profile", "👤"),
]


def go_to(page_name: str):
  st.session_state.page = page_name
  st.rerun()


def render_back_next():
  """Bottom navigation controls with professional styling."""
  names = [n for n, _ in NAV_ITEMS]
  idx = names.index(st.session_state.page)

  st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
  st.markdown(
      "<hr style='border: none; height: 1px; background: linear-gradient(90deg,"
      " transparent, rgba(255,255,255,0.12), transparent); margin-bottom:"
      " 28px;' />",
      unsafe_allow_html=True,
  )

  b1, spacer, b2 = st.columns([1, 2, 1])

  with b1:
    if idx > 0:
      prev_name, _ = NAV_ITEMS[idx - 1]
      if st.button(
          f"← {prev_name}", key="nav_back_btn", use_container_width=True
      ):
        go_to(prev_name)
    else:
      st.button(
          "← Previous",
          disabled=True,
          use_container_width=True,
          key="nav_back_disabled",
      )

  with b2:
    if idx < len(names) - 1:
      next_name, _ = NAV_ITEMS[idx + 1]
      if st.button(
          f"{next_name} →",
          key="nav_next_btn",
          use_container_width=True,
          type="primary",
      ):
        go_to(next_name)
    else:
      st.button(
          "Next →",
          disabled=True,
          use_container_width=True,
          key="nav_next_disabled",
      )


# =====================================
# ENTERPRISE GLASSMORPHISM & SHADOW CSS
# =====================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 15% 15%, #0f172a 0%, #090d16 50%, #030712 100%) !important;
    background-attachment: fixed !important;
}

/* Hide Streamlit default chrome */
#MainMenu, footer, header[data-testid="stHeader"],
div[data-testid="stToolbar"], div[data-testid="stDecoration"],
.stAppDeployButton {
    display: none !important;
}

/* Main Container Padding */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3.5rem;
    max-width: 1320px;
}

/* Topbar Header */
.topbar .eyebrow {
    color: #818cf8;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.topbar h1 {
    background: linear-gradient(135deg, #ffffff 30%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
}

.topbar .desc {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 6px;
}

/* Section Heading */
.section-heading {
    color: #f8fafc;
    font-size: 13px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 36px 0 18px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-heading .bar {
    width: 4px;
    height: 18px;
    border-radius: 6px;
    background: linear-gradient(180deg, #6366f1 0%, #a855f7 100%);
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.6);
    display: inline-block;
}

/* Premium Glassmorphic Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.45) 0%, rgba(15, 23, 42, 0.65) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 18px !important;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4), inset 0 1px 1px 0 rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
    border-color: rgba(129, 140, 248, 0.4) !important;
    box-shadow: 0 20px 35px -10px rgba(99, 102, 241, 0.22), inset 0 1px 1px 0 rgba(255, 255, 255, 0.2) !important;
}

/* KPI Components */
.kpi-card {
    position: relative;
    overflow: hidden;
}

.kpi-icon {
    width: 46px;
    height: 46px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.1) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    box-shadow: inset 0 0 12px rgba(99, 102, 241, 0.15);
    margin-bottom: 14px;
}

.kpi-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.kpi-value {
    color: #f8fafc;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 4px 0 8px 0;
}

.kpi-delta {
    display: inline-flex;
    align-items: center;
    color: #34d399;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.25);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
}

/* Feature Cards & Checklists */
.card-title {
    color: #f8fafc;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}

.card-sub {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 18px;
}

.feature-line {
    color: #cbd5e1;
    font-size: 13.5px;
    margin: 10px 0;
    display: flex;
    align-items: center;
}

.feature-line .tick {
    color: #10b981;
    background: rgba(16, 185, 129, 0.15);
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 800;
    margin-right: 12px;
}

.roadmap-line {
    color: #cbd5e1;
    font-size: 13.5px;
    margin: 12px 0;
    display: flex;
    align-items: center;
}

.roadmap-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.1) 100%);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 6px;
    font-size: 10px;
    font-weight: 800;
    padding: 3px 8px;
    margin-right: 12px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Sleek Buttons */
.stButton button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    padding: 10px 18px !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    color: #ffffff !important;
}

.stButton button[kind="primary"]:hover {
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
    transform: translateY(-1px);
}

.stButton button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #e2e8f0 !important;
}

.stButton button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: #070b14 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 0 26px 0;
}

.sidebar-brand .logo-badge {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
}

.sidebar-brand .brand-text {
    color: #f8fafc;
    font-weight: 800;
    font-size: 17px;
    letter-spacing: -0.01em;
}

.sidebar-brand .brand-sub {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
}

section[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #94a3b8 !important;
    justify-content: flex-start !important;
    padding: 10px 14px !important;
    border-radius: 10px !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.1) 100%) !important;
    color: #a5b4fc !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

/* Profile Section Sidebar */
.profile-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 14px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.profile-card .p-name {
    color: #f8fafc;
    font-weight: 700;
    font-size: 14px;
}

.profile-card .p-row {
    color: #64748b;
    font-size: 12px;
    margin-top: 2px;
}

.plan-badge {
    display: inline-block;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(52, 211, 153, 0.3);
    border-radius: 20px;
    font-size: 10px;
    font-weight: 800;
    padding: 2px 9px;
    margin-top: 4px;
}

.profile-avatar {
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    color: white;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
}

/* Profile Banner Main */
.profile-banner {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.08) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 22px;
    padding: 30px;
    display: flex;
    align-items: center;
    gap: 26px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px -5px rgba(0,0,0,0.3);
}

.profile-banner .p-name {
    color: #f8fafc;
    font-weight: 800;
    font-size: 24px;
    margin-bottom: 4px;
}

.profile-banner .p-tag {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 10px;
}

.skills-pill {
    display: inline-block;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #cbd5e1;
    font-size: 12px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 20px;
    margin: 4px 6px 4px 0;
}
</style>
""",
    unsafe_allow_html=True,
)


# =====================================
# HELPER: AVATAR RENDERER
# =====================================


def avatar_html(size=64, font_size=24):
  u = st.session_state.user
  if u.get("avatar_b64"):
    return (
        f'<img src="data:image/png;base64,{u["avatar_b64"]}" '
        f'style="width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;'
        'flex-shrink:0;box-shadow:0 6px 18px rgba(99,102,241,0.45);'
        ' border: 2px solid rgba(255,255,255,0.15);" />'
    )
  initial = u["name"].strip()[0].upper() if u.get("name") else "U"
  return (
      f'<div class="profile-avatar" style="width:{size}px;height:{size}px;'
      f'font-size:{font_size}px;">{initial}</div>'
  )


# =====================================
# AUTHENTICATION GATE
# =====================================

if not st.session_state.authenticated:
  st.markdown(
      """
        <div style="text-align:center; padding: 60px 0 24px 0;">
            <div class="topbar eyebrow" style="display:inline-block;">Enterprise Access</div>
            <h1 style="color:#f8fafc; font-size:38px; font-weight:800; margin:10px 0;">
                ⚡ AI Sentiment Intelligence Platform
            </h1>
            <div style="color:#94a3b8; font-size:15px;">
                Sign in to manage real-time sentiment metrics, insights, and datasets
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  _, mid, _ = st.columns([1, 1.1, 1])

  with mid:
    with st.container(border=True):
      tab_login, tab_signup = st.tabs(["🔐 Sign In", "✨ Register"])

      with tab_login:
        with st.form("login_form"):
          st.markdown("##### Welcome back")
          login_user = st.text_input("Username or Email")
          login_pass = st.text_input("Password", type="password")
          submitted = st.form_submit_button(
              "Sign In", use_container_width=True, type="primary"
          )

          if submitted:
            u = st.session_state.user
            if login_user.strip().lower() in (
                u["username"].lower(),
                u["email"].lower(),
            ) and login_pass == u["password_hash"]:
              st.session_state.authenticated = True
              st.rerun()
            else:
              st.error("Invalid credentials provided.")

        st.caption("Demo Account → **monika** / **changeme**")

      with tab_signup:
        with st.form("signup_form"):
          st.markdown("##### Create Account")
          su_name = st.text_input("Full Name")
          su_username = st.text_input("Username")
          su_email = st.text_input("Email")
          su_pass = st.text_input("Password", type="password")
          su_confirm = st.text_input("Confirm Password", type="password")
          su_submitted = st.form_submit_button(
              "Register", use_container_width=True, type="primary"
          )

          if su_submitted:
            if not (su_name and su_username and su_email and su_pass):
              st.error("All fields are required.")
            elif su_pass != su_confirm:
              st.error("Passwords do not match.")
            else:
              st.session_state.user.update({
                  "name": su_name,
                  "username": su_username,
                  "email": su_email,
                  "password_hash": su_pass,
                  "role": "Data Analyst",
                  "plan": "Free",
                  "bio": "New Platform User 👋",
              })
              st.session_state.authenticated = True
              st.rerun()

  st.stop()


# =====================================
# SIDEBAR
# =====================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="logo-badge">⚡</div>
        <div>
            <div class="brand-text">AI Platform</div>
            <div class="brand-sub">Sentiment Intelligence</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

for name, icon in NAV_ITEMS:
  is_active = st.session_state.page == name
  if st.sidebar.button(
      f"{icon}  {name}",
      key=f"nav_{name}",
      use_container_width=True,
      type="primary" if is_active else "secondary",
  ):
    if not is_active:
      go_to(name)

st.sidebar.markdown(
    "<hr style='border: none; height: 1px; background: linear-gradient(90deg,"
    " transparent, rgba(255,255,255,0.08), transparent); margin: 20px 0;' />",
    unsafe_allow_html=True,
)

_u = st.session_state.user
st.sidebar.markdown(
    f"""
    <div class="profile-card" style="display:flex; align-items:center; gap:12px;">
        {avatar_html(size=42, font_size=16)}
        <div>
            <div class="p-name">{_u['name']}</div>
            <div class="p-row">{_u['role']}</div>
            <div class="p-row"><span class="plan-badge">{_u['plan']} Member</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
if st.sidebar.button("🚪  Log Out", use_container_width=True):
  st.session_state.authenticated = False
  st.rerun()

st.sidebar.markdown(
    "<hr style='border: none; height: 1px; background: linear-gradient(90deg,"
    " transparent, rgba(255,255,255,0.08), transparent); margin: 20px 0;' />",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    '<div style="color:#475569; font-size:11px; text-align:center; font-weight:'
    ' 600;">AI Sentiment Intelligence v1.0</div>',
    unsafe_allow_html=True,
)


# =====================================
# DASHBOARD PAGE
# =====================================

if st.session_state.page == "Dashboard":

  top_l, top_r = st.columns([3, 1])
  with top_l:
    st.markdown(
        f"""
            <div class="topbar">
                <div class="eyebrow">Overview Dashboard</div>
                <h1>Welcome back, {_u['name'].split()[0]} 👋</h1>
                <div class="desc">Real-time sentiment insights and cross-channel intelligence.</div>
            </div>
            """,
        unsafe_allow_html=True,
    )
  with top_r:
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
    if st.button("🔄  Refresh Sync", use_container_width=True):
      st.toast("Platform data synchronized ✅")
    st.caption(
        "<div style='text-align:right;color:#64748b;font-size:11px;'>Updated"
        f" {datetime.now().strftime('%d %b, %I:%M %p')}</div>",
        unsafe_allow_html=True,
    )

  st.markdown(
      '<div class="section-heading"><span class="bar"></span>Metrics'
      " Overview</div>",
      unsafe_allow_html=True,
  )

  kpis = [
      ("👥", "Active Users", "1,245", "+4.2%"),
      ("📄", "Reports Generated", "2,891", "+7.8%"),
      ("🎥", "Videos Processed", "950", "+2.1%"),
      ("🏷️", "Topics Tracked", "760", "+5.4%"),
  ]
  kc = st.columns(4)
  for col, (icon, label, value, delta) in zip(kc, kpis):
    with col:
      with st.container(border=True):
        st.markdown(
            f"""
                    <div class="kpi-card">
                        <div class="kpi-icon">{icon}</div>
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                        <span class="kpi-delta">↑ {delta}</span>
                    </div>
                    """,
            unsafe_allow_html=True,
        )

  st.markdown(
      '<div class="section-heading"><span class="bar"></span>Intelligence'
      " Modules</div>",
      unsafe_allow_html=True,
  )

  m1, m2 = st.columns(2)

  with m1:
    with st.container(border=True):
      st.markdown(
          """
                <div class="card-title">🎥 YouTube Analysis</div>
                <div class="card-sub">Extract and evaluate real-time audience feedback</div>
                <div class="feature-line"><span class="tick">✓</span>Real-Time Comment Fetching</div>
                <div class="feature-line"><span class="tick">✓</span>TextBlob Sentiment Classification</div>
                <div class="feature-line"><span class="tick">✓</span>Word Cloud & KPI Summaries</div>
                """,
          unsafe_allow_html=True,
      )
      st.markdown(
          "<div style='height:14px;'></div>", unsafe_allow_html=True
      )
      if st.button(
          "Launch YouTube Analyzer →",
          key="open_yt",
          use_container_width=True,
          type="primary",
      ):
        go_to("YouTube Analysis")

  with m2:
    with st.container(border=True):
      st.markdown(
          """
                <div class="card-title">📰 News Intelligence</div>
                <div class="card-sub">Monitor global news coverage and media bias</div>
                <div class="feature-line"><span class="tick">✓</span>Global Topic Search</div>
                <div class="feature-line"><span class="tick">✓</span>Headlines Sentiment Scoring</div>
                <div class="feature-line"><span class="tick">✓</span>Trend Analytics & CSV Export</div>
                """,
          unsafe_allow_html=True,
      )
      st.markdown(
          "<div style='height:14px;'></div>", unsafe_allow_html=True
      )
      if st.button(
          "Launch News Intelligence →",
          key="open_news",
          use_container_width=True,
          type="primary",
      ):
        go_to("News Analysis")

  st.markdown(
      '<div class="section-heading"><span class="bar"></span>Platform'
      " Highlights & Roadmap</div>",
      unsafe_allow_html=True,
  )

  h1, h2 = st.columns(2)

  with h1:
    with st.container(border=True):
      st.markdown(
          """
                <div class="card-title">🚀 Core Capabilities</div>
                <div class="feature-line"><span class="tick">✓</span>Real-Time Multi-Source Ingestion</div>
                <div class="feature-line"><span class="tick">✓</span>NLP Sentiment Score Distribution</div>
                <div class="feature-line"><span class="tick">✓</span>Interactive Plotly Visualizations</div>
                <div class="feature-line"><span class="tick">✓</span>Exportable Analytics Reports</div>
                """,
          unsafe_allow_html=True,
      )

  with h2:
    with st.container(border=True):
      st.markdown(
          """
                <div class="card-title">🛣 Upcoming Features</div>
                <div class="roadmap-line"><span class="roadmap-badge">Q3 2026</span>AI Executive Summarization</div>
                <div class="roadmap-line"><span class="roadmap-badge">Q3 2026</span>Entity Recognition (NER)</div>
                <div class="roadmap-line"><span class="roadmap-badge">Q4 2026</span>Multi-Language Sentiment Support</div>
                """,
          unsafe_allow_html=True,
      )
      st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
      if st.button(
          "🔔 Subscribe to Feature Releases",
          key="notify_roadmap",
          use_container_width=True,
      ):
        st.toast("Notifications enabled for upcoming updates! 🎉")

  render_back_next()


# =====================================
# YOUTUBE PAGE
# =====================================

elif st.session_state.page == "YouTube Analysis":

  with open("dashboard/app.py", "r", encoding="utf-8") as f:
    exec(f.read())

  render_back_next()


# =====================================
# NEWS PAGE
# =====================================

elif st.session_state.page == "News Analysis":

  with open("dashboard/news_app.py", "r", encoding="utf-8") as f:
    exec(f.read())

  render_back_next()


# =====================================
# PROFILE PAGE
# =====================================

elif st.session_state.page == "Profile":

  u = st.session_state.user

  st.markdown(
      '<div class="topbar"><div class="eyebrow">Account Settings</div><h1>User'
      " Profile</h1></div>",
      unsafe_allow_html=True,
  )
  st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

  st.markdown(
      f"""
        <div class="profile-banner">
            {avatar_html(size=76, font_size=30)}
            <div>
                <div class="p-name">{u['name']}</div>
                <div class="p-tag">{u['bio']}</div>
                <span class="plan-badge">{u['plan']} Subscriber</span>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  tab_overview, tab_edit, tab_security = st.tabs(
      ["📋 Overview", "✏️ Edit Profile", "🔒 Security & Credentials"]
  )

  # OVERVIEW TAB
  with tab_overview:
    r1c1, r1c2, r1c3 = st.columns(3)

    with r1c1:
      with st.container(border=True):
        st.markdown(
            f"""
                    <div class="kpi-icon">💳</div>
                    <div class="card-title" style="font-size:15px;">Current Plan</div>
                    <div class="card-sub" style="margin-bottom:0;">{u['plan']} Tier · Renews monthly</div>
                    """,
            unsafe_allow_html=True,
        )

    with r1c2:
      with st.container(border=True):
        st.markdown(
            """
                    <div class="kpi-icon">📊</div>
                    <div class="card-title" style="font-size:15px;">Usage Statistics</div>
                    <div class="card-sub" style="margin-bottom:0;">2,891 queries processed</div>
                    """,
            unsafe_allow_html=True,
        )

    with r1c3:
      with st.container(border=True):
        st.markdown(
            f"""
                    <div class="kpi-icon">✉️</div>
                    <div class="card-title" style="font-size:15px;">Account Email</div>
                    <div class="card-sub" style="margin-bottom:0;">{u['email']}</div>
                    """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-heading"><span class="bar"></span>Developer Bio'
        " & Skills</div>",
        unsafe_allow_html=True,
    )

    skills_html = "".join(
        f'<span class="skills-pill">{s}</span>' for s in u["skills"]
    )
    with st.container(border=True):
      st.markdown(
          f'<div style="color:#cbd5e1;'
          f' font-size:14px;">{u["bio"]}</div><div'
          f' style="margin-top:16px;">{skills_html}</div>',
          unsafe_allow_html=True,
      )

  # EDIT PROFILE TAB
  with tab_edit:
    st.markdown("##### Profile Photo")
    pc1, pc2 = st.columns([1, 3])

    with pc1:
      st.markdown(avatar_html(size=88, font_size=32), unsafe_allow_html=True)

    with pc2:
      uploaded_photo = st.file_uploader(
          "Upload new avatar (PNG/JPG)", type=["png", "jpg", "jpeg"]
      )
      colp1, colp2 = st.columns(2)
      with colp1:
        if (
            uploaded_photo is not None
            and st.button("Save Photo", use_container_width=True, type="primary")
        ):
          st.session_state.user["avatar_b64"] = base64.b64encode(
              uploaded_photo.read()
          ).decode()
          st.success("Avatar updated!")
          st.rerun()
      with colp2:
        if u.get("avatar_b64") and st.button(
            "Remove Photo", use_container_width=True
        ):
          st.session_state.user["avatar_b64"] = None
          st.rerun()

    st.markdown(
        "<hr style='border: none; height: 1px; background:"
        " linear-gradient(90deg, transparent, rgba(255,255,255,0.08),"
        " transparent); margin:24px 0;' />",
        unsafe_allow_html=True,
    )

    with st.form("edit_profile_form"):
      st.markdown("##### Personal Information")
      new_name = st.text_input("Full Name", value=u["name"])
      new_username = st.text_input("Username", value=u["username"])
      new_email = st.text_input("Email Address", value=u["email"])
      new_role = st.text_input("Professional Title", value=u["role"])
      new_bio = st.text_area("Bio", value=u["bio"], height=80)
      new_skills = st.text_input(
          "Skills (comma separated)", value=", ".join(u["skills"])
      )

      if st.form_submit_button(
          "💾 Save Profile Changes", use_container_width=True, type="primary"
      ):
        st.session_state.user.update({
            "name": new_name.strip() or u["name"],
            "username": new_username.strip() or u["username"],
            "email": new_email.strip() or u["email"],
            "role": new_role.strip() or u["role"],
            "bio": new_bio.strip(),
            "skills": [s.strip() for s in new_skills.split(",") if s.strip()],
        })
        st.success("Profile updated successfully.")
        st.rerun()

  # SECURITY TAB
  with tab_security:
    with st.form("change_password_form"):
      st.markdown("##### Password Update")
      current_pw = st.text_input("Current Password", type="password")
      new_pw = st.text_input("New Password", type="password")
      confirm_pw = st.text_input("Confirm New Password", type="password")

      if st.form_submit_button(
          "Update Password", use_container_width=True, type="primary"
      ):
        if current_pw != st.session_state.user["password_hash"]:
          st.error("Current password is incorrect.")
        elif len(new_pw) < 4:
          st.error("Password must be at least 4 characters.")
        elif new_pw != confirm_pw:
          st.error("Passwords do not match.")
        else:
          st.session_state.user["password_hash"] = new_pw
          st.success("Password updated successfully.")

    st.markdown(
        "<hr style='border: none; height: 1px; background:"
        " linear-gradient(90deg, transparent, rgba(255,255,255,0.08),"
        " transparent); margin:24px 0;' />",
        unsafe_allow_html=True,
    )
    if st.button("🚪 Log Out of All Sessions"):
      st.session_state.authenticated = False
      st.rerun()

  render_back_next()