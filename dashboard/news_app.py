import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

from dotenv import load_dotenv
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI News Sentiment Dashboard",
    page_icon="📰",
    layout="wide"
)

# =====================================
# API CONFIG
# =====================================

load_dotenv()

# Env variable ya Streamlit Secrets dono jagah check karega
API_KEY = os.getenv("NEWS_API_KEY") or st.secrets.get("NEWS_API_KEY", "")

# =====================================
# HEADER
# =====================================

st.title("📰 AI News Sentiment Dashboard")

st.markdown(
    """
    Analyze real-time news sentiment using
    NLP and NewsAPI.
    """
)

# =====================================
# INPUT SECTION
# =====================================

topic = st.text_input(
    "🔍 Enter Topic",
    "Artificial Intelligence"
)

search_btn = st.button("Analyze News")

# =====================================
# MAIN LOGIC
# =====================================

if search_btn:

    with st.spinner("🔍 Fetching and Analyzing News..."):

        try:

            url = (
                f"https://newsapi.org/v2/everything?"
                f"q={topic}"
                f"&language=en"
                f"&sortBy=publishedAt"
                f"&pageSize=100"
                f"&apiKey={API_KEY}"
            )

            response = requests.get(url)
            data = response.json()

            # SAFE CHECK: Handle API Errors gracefully
            if response.status_code != 200:
                st.error(f"NewsAPI Error ({response.status_code}): {data.get('message', 'Failed to fetch news.')}")
                st.stop()

            articles_data = data.get("articles")
            if articles_data is None:
                st.error(f"API Response Error: {data.get('message', 'No articles key found in response.')}")
                st.stop()

            articles = []

            for article in articles_data:
                title = article.get("title")
                if title:
                    articles.append(title)

            if not articles:
                st.warning("No articles found for this topic.")
                st.stop()

            df = pd.DataFrame(articles, columns=["Headline"])

            st.success(f"Showing results for: {topic}")

            # =====================================
            # SENTIMENT ANALYSIS
            # =====================================

            def get_sentiment(text):
                score = TextBlob(text).sentiment.polarity
                if score > 0:
                    return "Positive"
                elif score < 0:
                    return "Negative"
                else:
                    return "Neutral"

            df["Sentiment"] = df["Headline"].apply(get_sentiment)

            # =====================================
            # KPI SECTION
            # =====================================

            total_news = len(df)
            positive = len(df[df["Sentiment"] == "Positive"])
            neutral = len(df[df["Sentiment"] == "Neutral"])
            negative = len(df[df["Sentiment"] == "Negative"])

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📰 Total News", total_news)
            c2.metric("😊 Positive", positive)
            c3.metric("😐 Neutral", neutral)
            c4.metric("😡 Negative", negative)

            # =====================================
            # CHART DATA
            # =====================================

            sentiment_counts = df["Sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]

            # =====================================
            # PIE + BAR CHARTS
            # =====================================

            left, right = st.columns(2)

            fig_pie = px.pie(
                sentiment_counts,
                values="Count",
                names="Sentiment",
                title=f"{topic} Sentiment Breakdown"
            )

            fig_bar = px.bar(
                sentiment_counts,
                x="Sentiment",
                y="Count",
                title=f"{topic} Sentiment Distribution"
            )

            with left:
                st.plotly_chart(fig_pie, use_container_width=True)

            with right:
                st.plotly_chart(fig_bar, use_container_width=True)

            # =====================================
            # WORD CLOUD
            # =====================================

            st.subheader("☁️ Word Cloud")
            text = " ".join(df["Headline"])

            wordcloud = WordCloud(
                width=1200,
                height=600,
                background_color="white"
            ).generate(text)

            fig_wc, ax = plt.subplots(figsize=(12, 6))
            ax.imshow(wordcloud)
            ax.axis("off")
            st.pyplot(fig_wc)

            # =====================================
            # POSITIVE & NEGATIVE NEWS
            # =====================================

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("😊 Top Positive News")
                st.dataframe(
                    df[df["Sentiment"] == "Positive"].head(10),
                    use_container_width=True
                )

            with col2:
                st.subheader("😡 Top Negative News")
                st.dataframe(
                    df[df["Sentiment"] == "Negative"].head(10),
                    use_container_width=True
                )

            # =====================================
            # AI INSIGHT
            # =====================================

            st.subheader("🤖 AI Insight")

            if positive > negative:
                st.success(f"Public sentiment around '{topic}' is mostly Positive.\n\nPositive News : {positive}\nNeutral News : {neutral}\nNegative News : {negative}")
            elif negative > positive:
                st.error(f"Public sentiment around '{topic}' is mostly Negative.\n\nPositive News : {positive}\nNeutral News : {neutral}\nNegative News : {negative}")
            else:
                st.info(f"Public sentiment around '{topic}' is Neutral.")

            # =====================================
            # FULL DATASET
            # =====================================

            st.subheader("📰 Full News Dataset")
            st.dataframe(df, use_container_width=True)

            # =====================================
            # DOWNLOAD REPORT
            # =====================================

            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Report",
                data=csv,
                file_name=f"{topic}_news_sentiment.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error: {e}")