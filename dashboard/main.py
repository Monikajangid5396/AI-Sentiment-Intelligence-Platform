import streamlit as st
import base64
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Sentiment Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
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
        "bio": "Final Year CSE Student · Aspiring Data Analyst · AI & NLP Enthusiast",
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

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin-bottom: 24px;' />", unsafe_allow_html=True)

    b1, spacer, b2 = st.columns([1, 2, 1])

    with b1:
        if idx > 0:
            prev_name, _ = NAV_ITEMS[idx - 1]
            if st.button(f"← {prev_name}", key="nav_back_btn", width="stretch"):
                go_to(prev_name)
        else:
            st.button("← Previous", disabled=True, width="stretch", key="nav_back_disabled")

    with b2:
        if idx < len(names) - 1:
            next_name, _ = NAV_ITEMS[idx + 1]
            if st.button(f"{next_name} →", key="nav_next_btn", width="stretch", type="primary"):
                go_to(next_name)
        else:
            st.button("Next →", disabled=True, width="stretch", key="nav_next_disabled")


# =====================================
# ENTERPRISE GLASSMORPHISM CSS
# =====================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at top right, #111827, #080c14);
}

/* Hide Streamlit default chrome */
#MainMenu, footer, header[data-testid="stHeader"],
div[data-testid="stToolbar"], div[data-testid="stDecoration"],
.stAppDeployButton {
    display: none !important;
}

/* Main Container Padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

/* Topbar Header */
.topbar .eyebrow {
    color: #6366f1;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.topbar h1 {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
}

.topbar .desc {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 4px;
}

/* Section Heading */
.section-heading {
    color: #f1f5f9;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-heading .bar {
    width: 4px;
    height: 16px;
    border-radius: 4px;
    background: linear-gradient(180deg, #6366f1, #a855f7);
    display: inline-block;
}

/* Glassmorphic Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 23, 42, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(12px);
    border-radius: 16px !important;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(99, 102, 241, 0.35) !important;
    box-shadow: 0 8px 25px -4px rgba(99, 102, 241, 0.15) !important;
}

/* KPI Components */
.kpi-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.2);
    margin-bottom: 12px;
}

.kpi-label {
    color: #64748b;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.kpi-value {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 4px 0 6px 0;
}

.kpi-delta {
    display: inline-flex;
    align-items: center;
    color: #10b981;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
}

/* Feature Checklists */
.card-title {
    color: #f8fafc;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 4px;
}

.card-sub {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 16px;
}

.feature-line {
    color: #cbd5e1;
    font-size: 13.5px;
    margin: 8px 0;
    display: flex;
    align-items: center;
}

.feature-line .tick {
    color: #10b981;
    font-weight: 800;
    margin-right: 10px;
}

.roadmap-line {
    color: #cbd5e1;
    font-size: 13.5px;
    margin: 10px 0;
    display: flex;
    align-items: center;
}

.roadmap-badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.12);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 6px;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 6px;
    margin-right: 10px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Buttons */
.stButton button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}

.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
}

.stButton button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    transform: translateY(-1px);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: #090d16 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 24px 0;
}

.sidebar-brand .logo-badge {
    background: linear-gradient(135deg, #6366f1, #a855f7);
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.sidebar-brand .brand-text {
    color: #f8fafc;
    font-weight: 800;
    font-size: 16px;
    letter-spacing: -0.01em;
}

.sidebar-brand .brand-sub {
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
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
    background: rgba(255, 255, 255, 0.04) !important;
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: rgba(99, 102, 241, 0.15) !important;
    color: #818cf8 !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    box-shadow: none !important;
}

/* Profile Section Sidebar */
.profile-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 14px;
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
    background: rgba(16, 185, 129, 0.12);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    margin-top: 4px;
}

.profile-avatar {
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: white;
    flex-shrink: 0;
}

/* Profile Banner Main */
.profile-banner {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12), rgba(168, 85, 247, 0.06));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 28px;
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 24px;
}

.profile-banner .p-name {
    color: #f8fafc;
    font-weight: 800;
    font-size: 22px;
    margin-bottom: 4px;
}

.profile-banner .p-tag {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 8px;
}

.skills-pill {
    display: inline-block;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 4px 6px 4px 0;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# HELPER: AVATAR RENDERER
# =====================================

def avatar_html(size=64, font_size=24):
    u = st.session_state.user
    if u.get("avatar_b64"):
        return (f'<img src="data:image/png;base64,{u["avatar_b64"]}" '
                f'style="width:{size}px;height:{size}px;border-radius:50%;object-fit:cover;'
                f'flex-shrink:0;box-shadow:0 4px 14px rgba(99,102,241,0.35);" />')
    initial = u["name"].strip()[0].upper() if u.get("name") else "U"
    return (f'<div class="profile-avatar" style="width:{size}px;height:{size}px;'
            f'font-size:{font_size}px;">{initial}</div>')


# =====================================
# AUTHENTICATION GATE
# =====================================

if not st.session_state.authenticated:
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 0 20px 0;">
            <div class="topbar eyebrow" style="display:inline-block;">Enterprise Access</div>
            <h1 style="color:#f8fafc; font-size:36px; font-weight:800; margin:8px 0 8px 0;">
                ⚡ AI Sentiment Intelligence Platform
            </h1>
            <div style="color:#94a3b8; font-size:15px;">
                Sign in to manage real-time sentiment metrics, insights, and datasets
            </div>
        </div>
        """,
        unsafe_allow_html=True
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
                    submitted = st.form_submit_button("Sign In", width="stretch", type="primary")

                    if submitted:
                        u = st.session_state.user
                        if login_user.strip().lower() in (u["username"].lower(), u["email"].lower()) \
                                and login_pass == u["password_hash"]:
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
                    su_submitted = st.form_submit_button("Register", width="stretch", type="primary")

                    if su_submitted:
                        if not (su_name and su_username and su_email and su_pass):
                            st.error("All fields are required.")
                        elif su_pass != su_confirm:
                            st.error("Passwords do not match.")
                        else:
                            st.session_state.user.update({
                                "name": su_name, "username": su_username, "email": su_email,
                                "password_hash": su_pass, "role": "Data Analyst", "plan": "Free",
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
    unsafe_allow_html=True
)

for name, icon in NAV_ITEMS:
    is_active = st.session_state.page == name
    if st.sidebar.button(
        f"{icon}  {name}",
        key=f"nav_{name}",
        width="stretch",
        type="primary" if is_active else "secondary",
    ):
        if not is_active:
            go_to(name)

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 20px 0;' />", unsafe_allow_html=True)

_u = st.session_state.user
st.sidebar.markdown(
    f"""
    <div class="profile-card" style="display:flex; align-items:center; gap:12px;">
        {avatar_html(size=40, font_size=16)}
        <div>
            <div class="p-name">{_u['name']}</div>
            <div class="p-row">{_u['role']}</div>
            <div class="p-row"><span class="plan-badge">{_u['plan']} Member</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
if st.sidebar.button("🚪  Log Out", width="stretch"):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 20px 0;' />", unsafe_allow_html=True)
st.sidebar.markdown('<div style="color:#475569; font-size:11px; text-align:center;">AI Sentiment Intelligence v1.0</div>', unsafe_allow_html=True)


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
            unsafe_allow_html=True
        )
    with top_r:
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        if st.button("🔄  Refresh Sync", width="stretch"):
            st.toast("Platform data synchronized ✅")
        st.caption(f"<div style='text-align:right;color:#475569;font-size:11px;'>Updated {datetime.now().strftime('%d %b, %I:%M %p')}</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="bar"></span>Metrics Overview</div>', unsafe_allow_html=True)

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
                    <div class="kpi-icon">{icon}</div>
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <span class="kpi-delta">↑ {delta}</span>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown('<div class="section-heading"><span class="bar"></span>Intelligence Modules</div>', unsafe_allow_html=True)

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
                unsafe_allow_html=True
            )
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            if st.button("Launch YouTube Analyzer →", key="open_yt", width="stretch", type="primary"):
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
                unsafe_allow_html=True
            )
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            if st.button("Launch News Intelligence →", key="open_news", width="stretch", type="primary"):
                go_to("News Analysis")

    st.markdown('<div class="section-heading"><span class="bar"></span>Platform Highlights & Roadmap</div>', unsafe_allow_html=True)

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
                unsafe_allow_html=True
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
                unsafe_allow_html=True
            )
            if st.button("🔔 Subscribe to Feature Releases", key="notify_roadmap", width="stretch"):
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

    st.markdown('<div class="topbar"><div class="eyebrow">Account Settings</div><h1>User Profile</h1></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="profile-banner">
            {avatar_html(size=72, font_size=28)}
            <div>
                <div class="p-name">{u['name']}</div>
                <div class="p-tag">{u['bio']}</div>
                <span class="plan-badge">{u['plan']} Subscriber</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
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
                    <div class="card-title" style="font-size:14px;">Current Plan</div>
                    <div class="card-sub" style="margin-bottom:0;">{u['plan']} Tier · Renews monthly</div>
                    """,
                    unsafe_allow_html=True
                )

        with r1c2:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="kpi-icon">📊</div>
                    <div class="card-title" style="font-size:14px;">Usage Statistics</div>
                    <div class="card-sub" style="margin-bottom:0;">2,891 queries processed</div>
                    """,
                    unsafe_allow_html=True
                )

        with r1c3:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="kpi-icon">✉️</div>
                    <div class="card-title" style="font-size:14px;">Account Email</div>
                    <div class="card-sub" style="margin-bottom:0;">{u['email']}</div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('<div class="section-heading"><span class="bar"></span>Developer Bio & Skills</div>', unsafe_allow_html=True)

        skills_html = "".join(f'<span class="skills-pill">{s}</span>' for s in u["skills"])
        with st.container(border=True):
            st.markdown(
                f'<div style="color:#cbd5e1; font-size:14px;">{u["bio"]}</div><div style="margin-top:14px;">{skills_html}</div>',
                unsafe_allow_html=True
            )

    # EDIT PROFILE TAB
    with tab_edit:
        st.markdown("##### Profile Photo")
        pc1, pc2 = st.columns([1, 3])

        with pc1:
            st.markdown(avatar_html(size=88, font_size=32), unsafe_allow_html=True)

        with pc2:
            uploaded_photo = st.file_uploader("Upload new avatar (PNG/JPG)", type=["png", "jpg", "jpeg"])
            colp1, colp2 = st.columns(2)
            with colp1:
                if uploaded_photo is not None and st.button("Save Photo", width="stretch", type="primary"):
                    st.session_state.user["avatar_b64"] = base64.b64encode(uploaded_photo.read()).decode()
                    st.success("Avatar updated!")
                    st.rerun()
            with colp2:
                if u.get("avatar_b64") and st.button("Remove Photo", width="stretch"):
                    st.session_state.user["avatar_b64"] = None
                    st.rerun()

        st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin:20px 0;' />", unsafe_allow_html=True)

        with st.form("edit_profile_form"):
            st.markdown("##### Personal Information")
            new_name = st.text_input("Full Name", value=u["name"])
            new_username = st.text_input("Username", value=u["username"])
            new_email = st.text_input("Email Address", value=u["email"])
            new_role = st.text_input("Professional Title", value=u["role"])
            new_bio = st.text_area("Bio", value=u["bio"], height=80)
            new_skills = st.text_input("Skills (comma separated)", value=", ".join(u["skills"]))

            if st.form_submit_button("💾 Save Profile Changes", width="stretch", type="primary"):
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

            if st.form_submit_button("Update Password", width="stretch", type="primary"):
                if current_pw != st.session_state.user["password_hash"]:
                    st.error("Current password is incorrect.")
                elif len(new_pw) < 4:
                    st.error("Password must be at least 4 characters.")
                elif new_pw != confirm_pw:
                    st.error("Passwords do not match.")
                else:
                    st.session_state.user["password_hash"] = new_pw
                    st.success("Password updated successfully.")

        st.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin:20px 0;' />", unsafe_allow_html=True)
        if st.button("🚪 Log Out of All Sessions"):
            st.session_state.authenticated = False
            st.rerun()

    render_back_next()