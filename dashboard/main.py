import streamlit as st
import base64
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Sentiment Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# =====================================
# SESSION STATE
# (acts as the logged-in user's profile store + current page.
#  In a real deployment "user" would be a DB row and "page" would be
#  actual routing — here it lives in st.session_state.)
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
        "password_hash": "changeme",   # demo only — replace with real hashing/DB in production
    }

if "authenticated" not in st.session_state:
    st.session_state.authenticated = True   # demo: visitor starts logged in

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

NAV_ITEMS = [
    ("Dashboard", "🏠"),
    ("YouTube Analysis", "🎥"),
    ("News Analysis", "📰"),
    ("Profile", "👤"),
]


def go_to(page_name: str):
    st.session_state.page = page_name
    st.rerun()


def render_back_next():
    """Bottom-of-page Back / Next controls that cycle through NAV_ITEMS in order."""
    names = [n for n, _ in NAV_ITEMS]
    idx = names.index(st.session_state.page)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    b1, spacer, b2 = st.columns([1, 2, 1])

    with b1:
        if idx > 0:
            prev_name, prev_icon = NAV_ITEMS[idx - 1]
            if st.button(f"←  Back: {prev_name}", key="nav_back_btn", use_container_width=True):
                go_to(prev_name)
        else:
            st.button("←  Back", disabled=True, use_container_width=True, key="nav_back_disabled")

    with b2:
        if idx < len(names) - 1:
            next_name, next_icon = NAV_ITEMS[idx + 1]
            if st.button(f"Next: {next_name}  →", key="nav_next_btn", use_container_width=True, type="primary"):
                go_to(next_name)
        else:
            st.button("Next  →", disabled=True, use_container_width=True, key="nav_next_disabled")


# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp{
    background: #0b0f19;
}

/* ---------- Hide Streamlit chrome (menu, footer, deploy toolbar) ---------- */
#MainMenu, footer, header[data-testid="stHeader"],
div[data-testid="stToolbar"], div[data-testid="stDecoration"],
.stAppDeployButton {
    display: none !important;
}

/* ---------- Layout ---------- */
.block-container{
    padding-top: 2rem;
    max-width: 1250px;
}

/* ---------- Top bar ---------- */
.topbar{
    display:flex;
    justify-content:space-between;
    align-items:flex-end;
    margin-bottom:26px;
}

.topbar .eyebrow{
    color:#818cf8;
    font-size:12px;
    font-weight:700;
    letter-spacing:0.08em;
    text-transform:uppercase;
    margin-bottom:6px;
}

.topbar h1{
    color:#f8fafc;
    font-size:28px;
    font-weight:800;
    letter-spacing:-0.02em;
    margin:0;
}

.topbar .desc{
    color:#8b93a7;
    font-size:14px;
    margin-top:4px;
}

.topbar .meta{
    text-align:right;
    color:#8b93a7;
    font-size:12.5px;
}

/* ---------- Section heading ---------- */
.section-heading{
    color:#e5e9f0;
    font-size:15px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.05em;
    margin:28px 0 14px 0;
    display:flex;
    align-items:center;
    gap:8px;
}

.section-heading .bar{
    width:3px;
    height:14px;
    border-radius:3px;
    background: linear-gradient(180deg, #818cf8, #a78bfa);
    display:inline-block;
}

/* ---------- Native bordered containers used as cards ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]{
    border-color: rgba(255,255,255,0.09) !important;
    background: #10151f;
    border-radius: 14px !important;
    transition: border-color 0.18s ease, transform 0.18s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(button):hover{
    border-color: rgba(129,140,248,0.45) !important;
}

/* ---------- KPI cards ---------- */
.kpi-icon{
    width:38px; height:38px;
    border-radius:10px;
    display:flex; align-items:center; justify-content:center;
    font-size:18px;
    background: rgba(129,140,248,0.12);
    margin-bottom:10px;
}

.kpi-label{
    color:#8b93a7;
    font-size:12.5px;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:0.04em;
}

.kpi-value{
    color:#f8fafc;
    font-size:28px;
    font-weight:800;
    margin:4px 0 6px 0;
}

.kpi-delta{
    display:inline-block;
    color:#34d399;
    background:rgba(52,211,153,0.12);
    border-radius:6px;
    font-size:11.5px;
    font-weight:700;
    padding:2px 8px;
}

/* ---------- Feature checklist ---------- */
.feature-line{
    color:#c3c9d6;
    font-size:14.5px;
    margin:7px 0;
}
.feature-line .tick{ color:#34d399; font-weight:700; margin-right:8px; }

.roadmap-line{
    color:#c3c9d6;
    font-size:14.5px;
    margin:8px 0;
}
.roadmap-badge{
    display:inline-block;
    background:rgba(251,191,36,0.12);
    color:#fbbf24;
    border-radius:6px;
    font-size:10.5px;
    font-weight:700;
    padding:2px 7px;
    margin-right:9px;
    letter-spacing:0.03em;
    text-transform:uppercase;
}

.card-title{
    color:#f8fafc;
    font-size:16px;
    font-weight:700;
    margin-bottom:2px;
}
.card-sub{
    color:#6b7385;
    font-size:12.5px;
    margin-bottom:14px;
}

/* ---------- Buttons ---------- */
.stButton button{
    border-radius:9px !important;
    font-weight:600 !important;
    font-size:13.5px !important;
}
.stButton button[kind="primary"]{
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border:none !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
    background:#0a0e17;
    border-right:1px solid rgba(255,255,255,0.06);
}

.sidebar-brand{
    display:flex; align-items:center; gap:10px;
    padding: 2px 0 20px 0;
}
.sidebar-brand .logo-badge{
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    width:36px; height:36px; border-radius:9px;
    display:flex; align-items:center; justify-content:center;
    font-size:17px;
}
.sidebar-brand .brand-text{ color:#f8fafc; font-weight:800; font-size:16px; line-height:1.1; }
.sidebar-brand .brand-sub{ color:#5c6478; font-size:10.5px; font-weight:500; }

/* sidebar nav buttons */
section[data-testid="stSidebar"] .stButton button{
    background: transparent !important;
    border: 1px solid transparent !important;
    color:#a2a9ba !important;
    text-align:left !important;
    justify-content:flex-start !important;
    padding: 9px 12px !important;
    font-weight:500 !important;
}
section[data-testid="stSidebar"] .stButton button:hover{
    background: rgba(255,255,255,0.05) !important;
    color:#f8fafc !important;
}
section[data-testid="stSidebar"] .stButton button[kind="primary"]{
    background: rgba(99,102,241,0.16) !important;
    color:#c7d2fe !important;
    border:1px solid rgba(99,102,241,0.35) !important;
}

.profile-card{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;
    padding:12px 14px;
    margin-top:6px;
}
.profile-card .p-name{ color:#f8fafc; font-weight:700; font-size:14px; }
.profile-card .p-row{ color:#8b93a7; font-size:12px; margin-top:2px; }
.plan-badge{
    display:inline-block;
    background:rgba(52,211,153,0.14);
    color:#34d399;
    border-radius:999px;
    font-size:10.5px;
    font-weight:700;
    padding:1px 9px;
    margin-top:4px;
}
.sidebar-footer{ color:#3d4356; font-size:11px; text-align:center; }

.profile-avatar{
    border-radius:50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display:flex; align-items:center; justify-content:center;
    font-weight:700; color:white; flex-shrink:0;
}

/* ---------- Profile banner ---------- */
.profile-banner{
    background: linear-gradient(120deg, rgba(99,102,241,0.14), rgba(139,92,246,0.08));
    border:1px solid rgba(255,255,255,0.09);
    border-radius:16px;
    padding:24px 28px;
    display:flex; align-items:center; gap:20px;
    margin-bottom:20px;
}
.profile-banner .p-name{ color:#f8fafc; font-weight:800; font-size:20px; margin-bottom:4px; }
.profile-banner .p-tag{ color:#8b93a7; font-size:13px; }

.skills-pill{
    display:inline-block;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
    color:#c3c9d6;
    font-size:12px;
    font-weight:600;
    padding:4px 12px;
    border-radius:999px;
    margin:4px 6px 4px 0;
}

hr{ border-color: rgba(255,255,255,0.08) !important; }

</style>
""", unsafe_allow_html=True)


# =====================================
# HELPER: avatar (uploaded photo if present, else initials)
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
# LOGIN / SIGNUP GATE
# =====================================

if not st.session_state.authenticated:

    st.markdown(
        """
        <div style="text-align:center; padding: 40px 0 10px 0;">
            <div class="topbar eyebrow" style="display:inline-block;">Secure Access</div>
            <h1 style="color:#f8fafc; font-size:34px; font-weight:800; margin:8px 0 6px 0;">
                📊 AI Sentiment Intelligence Platform
            </h1>
            <div style="color:#8b93a7; font-size:15px;">
                Sign in to access your dashboard, reports and saved analyses
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, mid, right = st.columns([1, 1.1, 1])

    with mid:
        with st.container(border=True):
            tab_login, tab_signup = st.tabs(["🔐 Log In", "✨ Sign Up"])

            with tab_login:
                with st.form("login_form"):
                    st.markdown("##### Welcome back")
                    login_user = st.text_input("Username or Email")
                    login_pass = st.text_input("Password", type="password")
                    submitted = st.form_submit_button("Log In", use_container_width=True, type="primary")

                    if submitted:
                        u = st.session_state.user
                        if login_user.strip().lower() in (u["username"].lower(), u["email"].lower()) \
                                and login_pass == u["password_hash"]:
                            st.session_state.authenticated = True
                            st.rerun()
                        else:
                            st.error("Incorrect username/email or password.")

                st.caption("Demo credentials → username: **monika**, password: **changeme**")

            with tab_signup:
                with st.form("signup_form"):
                    st.markdown("##### Create your account")
                    su_name = st.text_input("Full Name")
                    su_username = st.text_input("Choose a Username")
                    su_email = st.text_input("Email")
                    su_pass = st.text_input("Create Password", type="password")
                    su_confirm = st.text_input("Confirm Password", type="password")
                    su_submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")

                    if su_submitted:
                        if not (su_name and su_username and su_email and su_pass):
                            st.error("Please fill in all fields.")
                        elif su_pass != su_confirm:
                            st.error("Passwords do not match.")
                        else:
                            st.session_state.user.update({
                                "name": su_name, "username": su_username, "email": su_email,
                                "password_hash": su_pass, "role": "Data Analyst", "plan": "Free",
                                "bio": "New member 👋",
                            })
                            st.session_state.authenticated = True
                            st.success("Account created! Redirecting...")
                            st.rerun()

    st.stop()


# =====================================
# SIDEBAR
# =====================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="logo-badge">🚀</div>
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
        use_container_width=True,
        type="primary" if is_active else "secondary",
    ):
        if not is_active:
            go_to(name)

st.sidebar.markdown("---")

_u = st.session_state.user
st.sidebar.markdown(
    f"""
    <div class="profile-card" style="display:flex; align-items:center; gap:12px;">
        {avatar_html(size=40, font_size=16)}
        <div>
            <div class="p-name">{_u['name']}</div>
            <div class="p-row">{_u['role']}</div>
            <div class="p-row">Plan: <span class="plan-badge">{_u['plan']}</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("🚪  Log Out", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="sidebar-footer">AI Sentiment Intelligence Platform · v1.0</div>', unsafe_allow_html=True)


# =====================================
# DASHBOARD
# =====================================

if st.session_state.page == "Dashboard":

    top_l, top_r = st.columns([3, 1])
    with top_l:
        st.markdown(
            f"""
            <div class="topbar eyebrow">Overview</div>
            <h1>Welcome back, {_u['name'].split()[0]} 👋</h1>
            <div class="desc">Here's what's happening across your sentiment intelligence workspace.</div>
            """,
            unsafe_allow_html=True
        )
    with top_r:
        st.markdown("<div style='margin-top:22px;'></div>", unsafe_allow_html=True)
        if st.button("🔄  Refresh Data", use_container_width=True):
            st.toast("Data refreshed just now ✅")
        st.caption(f"<div style='text-align:right;color:#5c6478;font-size:11.5px;'>Updated {datetime.now().strftime('%d %b, %I:%M %p')}</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-heading"><span class="bar"></span>Platform Statistics</div>', unsafe_allow_html=True)

    kpis = [
        ("👥", "Users", "1,245", "+4.2%"),
        ("📄", "Reports", "2,891", "+7.8%"),
        ("🎬", "Videos", "950", "+2.1%"),
        ("🏷️", "Topics", "760", "+5.4%"),
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

    st.markdown('<div class="section-heading"><span class="bar"></span>Core Modules</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)

    with m1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="card-title">🎥 YouTube Analysis</div>
                <div class="card-sub">Real-time comment sentiment for any video</div>
                <div class="feature-line"><span class="tick">✔</span>Real-Time Comment Analysis</div>
                <div class="feature-line"><span class="tick">✔</span>Sentiment Detection</div>
                <div class="feature-line"><span class="tick">✔</span>Word Cloud & AI Insights</div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Open YouTube Analysis  →", key="open_yt", use_container_width=True, type="primary"):
                go_to("YouTube Analysis")

    with m2:
        with st.container(border=True):
            st.markdown(
                """
                <div class="card-title">📰 News Intelligence</div>
                <div class="card-sub">Track sentiment and trends across news topics</div>
                <div class="feature-line"><span class="tick">✔</span>Topic Search</div>
                <div class="feature-line"><span class="tick">✔</span>News Sentiment Analysis</div>
                <div class="feature-line"><span class="tick">✔</span>Trend Detection & AI Insights</div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Open News Analysis  →", key="open_news", use_container_width=True, type="primary"):
                go_to("News Analysis")

    st.markdown('<div class="section-heading"><span class="bar"></span>Platform Highlights & Roadmap</div>', unsafe_allow_html=True)

    h1, h2 = st.columns(2)

    with h1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="card-title">🤖 Platform Highlights</div>
                <div class="feature-line"><span class="tick">✔</span>Real-Time Sentiment Analytics</div>
                <div class="feature-line"><span class="tick">✔</span>NLP Powered Insights</div>
                <div class="feature-line"><span class="tick">✔</span>Interactive Dashboards</div>
                <div class="feature-line"><span class="tick">✔</span>Downloadable Reports</div>
                <div class="feature-line"><span class="tick">✔</span>YouTube + News Intelligence</div>
                """,
                unsafe_allow_html=True
            )

    with h2:
        with st.container(border=True):
            st.markdown(
                """
                <div class="card-title">🛣 Future Roadmap</div>
                <div class="roadmap-line"><span class="roadmap-badge">Soon</span>AI Executive Summary</div>
                <div class="roadmap-line"><span class="roadmap-badge">Soon</span>Trending Keyword Analysis</div>
                <div class="roadmap-line"><span class="roadmap-badge">Soon</span>Topic Comparison</div>
                <div class="roadmap-line"><span class="roadmap-badge">Soon</span>Report History</div>
                <div class="roadmap-line"><span class="roadmap-badge">Soon</span>Advanced Analytics</div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🔔  Notify me when these ship", key="notify_roadmap", use_container_width=True):
                st.toast("You'll be notified as soon as new features launch! 🎉")

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

    st.markdown('<div class="topbar eyebrow">Account</div><h1>Your Account</h1>', unsafe_allow_html=True)
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="profile-banner">
            {avatar_html(size=64, font_size=26)}
            <div>
                <div class="p-name">{u['name']}</div>
                <div class="p-tag">{u['bio']}</div>
                <span class="plan-badge">{u['plan']} Member</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_overview, tab_edit, tab_security = st.tabs(
        ["📋 Overview", "✏️ Edit Profile", "🔒 Login & Security"]
    )

    # ---------------- OVERVIEW ----------------
    with tab_overview:

        r1c1, r1c2, r1c3 = st.columns(3)

        with r1c1:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="kpi-icon">💳</div>
                    <div class="card-title" style="font-size:14.5px;">Your Plan</div>
                    <div class="card-sub" style="margin-bottom:0;">{u['plan']} Plan · Renews monthly</div>
                    """,
                    unsafe_allow_html=True
                )

        with r1c2:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="kpi-icon">📊</div>
                    <div class="card-title" style="font-size:14.5px;">Reports & Activity</div>
                    <div class="card-sub" style="margin-bottom:0;">2,891 reports generated so far</div>
                    """,
                    unsafe_allow_html=True
                )
                with st.expander("View recent activity"):
                    st.markdown(
                        "- 🎥 YouTube analysis — *Tech Review #452* — 2 hours ago\n"
                        "- 📰 News topic tracked — *AI Regulation* — yesterday\n"
                        "- 🎥 YouTube analysis — *Product Launch Reaction* — 3 days ago"
                    )

        with r1c3:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="kpi-icon">✉️</div>
                    <div class="card-title" style="font-size:14.5px;">Contact Email</div>
                    <div class="card-sub" style="margin-bottom:0;">{u['email']}</div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('<div class="section-heading"><span class="bar"></span>About</div>', unsafe_allow_html=True)

        skills_html = "".join(f'<span class="skills-pill">{s}</span>' for s in u["skills"])
        with st.container(border=True):
            st.markdown(
                f'<div class="feature-line">{u["bio"]}</div><div style="margin-top:12px;">{skills_html}</div>',
                unsafe_allow_html=True
            )

    # ---------------- EDIT PROFILE ----------------
    with tab_edit:

        st.markdown("##### Profile Photo")
        pc1, pc2 = st.columns([1, 3])

        with pc1:
            st.markdown(avatar_html(size=88, font_size=32), unsafe_allow_html=True)

        with pc2:
            uploaded_photo = st.file_uploader("Upload a new photo (JPG/PNG)", type=["png", "jpg", "jpeg"])
            colp1, colp2 = st.columns(2)
            with colp1:
                if uploaded_photo is not None and st.button("Save Photo", use_container_width=True, type="primary"):
                    st.session_state.user["avatar_b64"] = base64.b64encode(uploaded_photo.read()).decode()
                    st.success("Profile photo updated.")
                    st.rerun()
            with colp2:
                if u.get("avatar_b64") and st.button("Remove Photo", use_container_width=True):
                    st.session_state.user["avatar_b64"] = None
                    st.rerun()

        st.markdown("---")
        st.markdown("##### Personal Details")

        with st.form("edit_profile_form"):
            new_name = st.text_input("Full Name", value=u["name"])
            new_username = st.text_input("Username", value=u["username"])
            new_email = st.text_input("Email", value=u["email"])
            new_role = st.text_input("Role / Title", value=u["role"])
            new_bio = st.text_area("Bio", value=u["bio"], height=80)
            new_skills = st.text_input("Skills (comma separated)", value=", ".join(u["skills"]))

            if st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary"):
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

    # ---------------- LOGIN & SECURITY ----------------
    with tab_security:

        st.markdown("##### Change Password")

        with st.form("change_password_form"):
            current_pw = st.text_input("Current Password", type="password")
            new_pw = st.text_input("New Password", type="password")
            confirm_pw = st.text_input("Confirm New Password", type="password")

            if st.form_submit_button("Update Password", use_container_width=True, type="primary"):
                if current_pw != st.session_state.user["password_hash"]:
                    st.error("Current password is incorrect.")
                elif len(new_pw) < 4:
                    st.error("New password must be at least 4 characters.")
                elif new_pw != confirm_pw:
                    st.error("New password and confirmation do not match.")
                else:
                    st.session_state.user["password_hash"] = new_pw
                    st.success("Password updated successfully.")

        st.markdown("---")
        st.markdown("##### Account")
        st.caption(f"Signed in as **{u['username']}** ({u['email']})")

        if st.button("🚪 Log Out of All Devices"):
            st.session_state.authenticated = False
            st.rerun()

        st.caption(
            "⚠️ Demo note: passwords and photos live only in this session's memory, "
            "not a real database — connect a backend (with hashed passwords) before production."
        )

    render_back_next()