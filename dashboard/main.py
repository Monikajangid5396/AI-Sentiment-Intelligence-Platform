import streamlit as st

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Sentiment Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #111827
    );
}

.main-title{
    font-size:55px;
    font-weight:800;
    text-align:center;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:20px;
    margin-bottom:30px;
}

.glass-card{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:20px;
    padding:25px;
    color:white;
    margin-bottom:20px;
}

section[data-testid="stSidebar"]{
    background:#0b1120;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🚀 AI Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎥 YouTube Analysis",
        "📰 News Analysis",
        "👤 Profile"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    👤 Monika

    Role: Data Analyst

    Plan: Premium
    """
)

# =====================================
# DASHBOARD
# =====================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="main-title">
        📊 AI Sentiment Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
        Real-Time Public Opinion Analytics using NLP
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # KPI SECTION

    st.subheader("📈 Platform Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Users",
        "1,245"
    )

    c2.metric(
        "Reports",
        "2,891"
    )

    c3.metric(
        "Videos",
        "950"
    )

    c4.metric(
        "Topics",
        "760"
    )

    st.markdown("---")

    # FEATURE CARDS

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="glass-card">

            <h2>🎥 YouTube Analysis</h2>

            ✔ Real-Time Comment Analysis

            ✔ Sentiment Detection

            ✔ Word Cloud

            ✔ AI Insights

            ✔ KPI Dashboard

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="glass-card">

            <h2>📰 News Intelligence</h2>

            ✔ Topic Search

            ✔ News Sentiment Analysis

            ✔ Trend Detection

            ✔ Word Cloud

            ✔ AI Insights

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        """
        <div class="glass-card">

        <h2>🤖 Platform Highlights</h2>

        • Real-Time Sentiment Analytics

        • NLP Powered Insights

        • Interactive Dashboards

        • Downloadable Reports

        • YouTube + News Intelligence

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-card">

        <h2>🛣 Future Roadmap</h2>

        🚧 AI Executive Summary

        🚧 Trending Keyword Analysis

        🚧 Topic Comparison

        🚧 Report History

        🚧 User Authentication

        🚧 Advanced Analytics

        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# YOUTUBE PAGE
# =====================================

elif page == "🎥 YouTube Analysis":

    with open(
        "dashboard/app.py",
        "r",
        encoding="utf-8"
    ) as f:

        exec(f.read())

# =====================================
# NEWS PAGE
# =====================================

elif page == "📰 News Analysis":

    with open(
        "dashboard/news_app.py",
        "r",
        encoding="utf-8"
    ) as f:

        exec(f.read())

# =====================================
# PROFILE PAGE
# =====================================

elif page == "👤 Profile":

    st.title("👤 User Profile")

    st.markdown(
        """
        <div class="glass-card">

        <h2>Monika Jangid</h2>

        🎓 Final Year CSE Student

        📊 Aspiring Data Analyst

        🐍 Python | SQL | Power BI

        🤖 AI & NLP Enthusiast

        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# FOOTER
# =====================================

st.sidebar.markdown("---")

st.sidebar.caption(
    "AI Sentiment Intelligence Platform v1.0"
)