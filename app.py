import streamlit as st
import pandas as pd

from news_fetch import fetch_news
from predict_esg import predict_category
from sentiment import analyze_sentiment
from esg_update import update_esg
from stock_predict import predict_stock
from visualise import plot_esg
from recommend import recommend_similar


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Real-Time ESG Impact Tracker",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
df = pd.read_csv("data/esg_companies.csv")

score_cols = [
    "Environment Risk Score",
    "Social Risk Score",
    "Governance Risk Score",
    "Total ESG Risk score"
]

df[score_cols] = df[score_cols].apply(pd.to_numeric, errors="coerce")
df[score_cols] = df[score_cols].fillna(df[score_cols].mean())


# -------------------- UI HEADER --------------------
st.title("Real-Time ESG Impact Tracker")
st.markdown(
    "Analyze real-time ESG impact of companies using live news"
)

st.divider()


# -------------------- INPUT --------------------
company = st.text_input("Enter Company Name")

if st.button("Analyze ESG Impact"):

    if company not in df["Name"].values:
        st.error("Company not found in dataset.")
    else:
        row = df[df["Name"] == company].iloc[0]

        # -------------------- BASE SCORES --------------------
        base = {
            "E": row["Environment Risk Score"],
            "S": row["Social Risk Score"],
            "G": row["Governance Risk Score"],
            "ESG": row["Total ESG Risk score"]
        }

        # -------------------- FETCH NEWS --------------------
        with st.spinner("Fetching real-time news..."):
            news = fetch_news(company)

        results = []
        for n in news:
            cat = predict_category(n)
            sent, score = analyze_sentiment(n)
            results.append({
                "category": cat,
                "sentiment": sent,
                "score": score
            })

        # -------------------- UPDATE ESG --------------------
        updated = update_esg(base, results)

        # -------------------- DISPLAY SCORES --------------------
        st.subheader("ESG Scores Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("Yesterday")
            st.metric("Environmental", base["E"])
            st.metric("Social", base["S"])
            st.metric("Governance", base["G"])
            st.metric("Total ESG", base["ESG"])

        with col2:
            st.markdown("Today")
            st.metric("Environmental", updated["E"])
            st.metric("Social", updated["S"])
            st.metric("Governance", updated["G"])
            st.metric("Total ESG", updated["ESG"])

        # -------------------- ESG TREND GRAPH --------------------
        st.subheader("ESG Score Trend")

        left, center, right = st.columns([1, 2, 1])
        with center:
            st.pyplot(plot_esg(base["ESG"], updated["ESG"]))

        # -------------------- STOCK OUTLOOK --------------------
        st.subheader("Stock Outlook Prediction")

        outlook = predict_stock(base, updated)

        if "fall" in outlook.lower():
            st.error(outlook)
        elif "rise" in outlook.lower():
            st.success(outlook)
        else:
            st.info(outlook)

        # -------------------- SIMILAR COMPANIES --------------------
        st.subheader("Companies with Similar ESG Profile")

        similar = recommend_similar(
            df,
            [
                row["Environment Risk Score"],
                row["Social Risk Score"],
                row["Governance Risk Score"]
            ]
        )

        st.dataframe(similar.reset_index(drop=True), use_container_width=True)
