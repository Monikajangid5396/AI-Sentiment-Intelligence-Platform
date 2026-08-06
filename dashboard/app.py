import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from textblob import TextBlob

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="YouTube Sentiment Analyzer",
    page_icon="🎥",
    layout="wide"
)

# =====================================
# API CONFIG
# =====================================

load_dotenv()

API_KEY = os.getenv(
    "YOUTUBE_API_KEY"
)

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# =====================================
# SENTIMENT FUNCTIONS
# =====================================

def get_sentiment(text):

    score = TextBlob(text).sentiment.polarity

    if score > 0:
        return "Positive"

    elif score < 0:
        return "Negative"

    else:
        return "Neutral"


def sentiment_score(text):

    return TextBlob(text).sentiment.polarity

def get_video_id(url):
    parsed = urlparse(url)

    # https://youtu.be/VIDEO_ID
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    # https://www.youtube.com/watch?v=VIDEO_ID
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):

        if parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            if "v" in qs:
                return qs["v"][0]

        # https://youtube.com/shorts/VIDEO_ID
        if parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

        # https://youtube.com/embed/VIDEO_ID
        if parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]

    raise ValueError("Invalid YouTube URL")


# =====================================
# HEADER
# =====================================

st.title(
    "🎥 AI YouTube Sentiment Dashboard"
)

st.markdown(
    """
    Analyze YouTube audience sentiment
    using NLP and Real-Time Comments.
    """
)

# =====================================
# URL INPUT
# =====================================

video_url = st.text_input(
    "🔗 Paste YouTube Video URL"
)

analyze_btn = st.button(
    "Analyze Video"
)

# =====================================
# MAIN LOGIC
# =====================================

if analyze_btn:

    with st.spinner("🔍 Analyzing Comments..."):

        try:

            video_id = get_video_id(video_url)

            st.success(
                f"Video ID: {video_id}"
            )

            # FETCH COMMENTS

            comments = []

            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText"
            )

            response = request.execute()

            for item in response["items"]:

                comment = item["snippet"][
                    "topLevelComment"
                ]["snippet"]["textDisplay"]

                comments.append(comment)

            # DATAFRAME

            df = pd.DataFrame(
                comments,
                columns=["Comment"]
            )

            # SENTIMENT

            df["Sentiment"] = df["Comment"].apply(
                get_sentiment
            )

            df["Score"] = df["Comment"].apply(
                sentiment_score
            )

            # KPI

            total_comments = len(df)

            positive_count = len(
                df[df["Sentiment"] == "Positive"]
            )

            neutral_count = len(
                df[df["Sentiment"] == "Neutral"]
            )

            negative_count = len(
                df[df["Sentiment"] == "Negative"]
            )

            avg_score = round(
                df["Score"].mean(),
                2
            )

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("Comments", total_comments)
            col2.metric("Positive", positive_count)
            col3.metric("Neutral", neutral_count)
            col4.metric("Negative", negative_count)
            col5.metric("Avg Score", avg_score)

            # CHARTS

            sentiment_counts = (
                df["Sentiment"]
                .value_counts()
                .reset_index()
            )

            sentiment_counts.columns = [
                "Sentiment",
                "Count"
            ]

            fig_pie = px.pie(
                sentiment_counts,
                values="Count",
                names="Sentiment",
                title="Sentiment Breakdown"
            )

            fig_bar = px.bar(
                sentiment_counts,
                x="Sentiment",
                y="Count",
                title="Sentiment Distribution"
            )

            left, right = st.columns(2)

            with left:

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True
                )

            with right:

                st.plotly_chart(
                    fig_bar,
                    use_container_width=True
                )

            # WORD CLOUD

            st.subheader("☁️ Word Cloud")

            text = " ".join(df["Comment"])

            wordcloud = WordCloud(
                width=1000,
                height=500,
                background_color="white"
            ).generate(text)

            fig, ax = plt.subplots(
                figsize=(12, 6)
            )

            ax.imshow(wordcloud)

            ax.axis("off")

            st.pyplot(fig)

            # POSITIVE & NEGATIVE COMMENTS

            positive_comments = (
                df[df["Sentiment"] == "Positive"]
                .sort_values(
                    by="Score",
                    ascending=False
                )
            )

            negative_comments = (
                df[df["Sentiment"] == "Negative"]
                .sort_values(
                    by="Score"
                )
            )

            c1, c2 = st.columns(2)

            with c1:

                st.subheader(
                    "😊 Positive Comments"
                )

                st.dataframe(
                    positive_comments[
                        ["Comment", "Score"]
                    ].head(10),
                    use_container_width=True
                )

            with c2:

                st.subheader(
                    "😡 Negative Comments"
                )

                st.dataframe(
                    negative_comments[
                        ["Comment", "Score"]
                    ].head(10),
                    use_container_width=True
                )

            # AI INSIGHT

            st.subheader(
                "🤖 AI Insight"
            )

            if avg_score > 0:

                st.success(
                    f"""
Audience sentiment is mostly Positive.

Positive Comments : {positive_count}
Neutral Comments  : {neutral_count}
Negative Comments : {negative_count}

Average Score : {avg_score}
"""
                )

            elif avg_score < 0:

                st.error(
                    f"""
Audience sentiment is mostly Negative.

Positive Comments : {positive_count}
Neutral Comments  : {neutral_count}
Negative Comments : {negative_count}

Average Score : {avg_score}
"""
                )

            else:

                st.info(
                    "Audience sentiment is Neutral."
                )

            # DATASET

            st.subheader(
                "📄 Full Comment Dataset"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # DOWNLOAD

            csv = df.to_csv(
                index=False
            )

            st.download_button(
                label="📥 Download Analysis Report",
                data=csv,
                file_name="youtube_sentiment_report.csv",
                mime="text/csv"
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )