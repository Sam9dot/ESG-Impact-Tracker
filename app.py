import streamlit as st
import pandas as pd
from news_fetch import fetch_news
from predict_esg import predict_category
from sentiment import analyze_sentiment
from esg_update import update_esg
from stock_predict import predict_stock
from visualise import plot_esg
from recommend import recommend_similar
#check esg formula,api test, prediction of rise/fall how, esg impact how, graph how, similar companies how, make frontend better,tfidf
df = pd.read_csv("data/esg_companies.csv")
score_cols = [
    "Environment Risk Score",
    "Social Risk Score",
    "Governance Risk Score",
    "Total ESG Risk score"
]

df[score_cols] = df[score_cols].fillna(df[score_cols].mean())

st.title("Real-Time ESG Impact Tracker")

company = st.text_input("Enter Company Name")

if st.button("Analyze"):
    row = df[df["Name"] == company].iloc[0]

    base = {
        "E": row["Environment Risk Score"],
        "S": row["Social Risk Score"],
        "G": row["Governance Risk Score"],
        "ESG": row["Total ESG Risk score"]
    }

    news = fetch_news(company)
    results = []

    for n in news:
        cat = predict_category(n)
        sent, score = analyze_sentiment(n)
        results.append({"category": cat, "sentiment": sent, "score": score})

    updated = update_esg(base, results)

    st.subheader("ESG Scores")
    st.write("Yesterday:", base)
    st.write("Today:", updated)

    st.subheader("ESG Trend")
    st.pyplot(plot_esg(base["ESG"], updated["ESG"]))

    st.subheader("Stock Outlook")
    st.write(predict_stock(base, updated))

    st.subheader("Similar Companies")
    st.dataframe(recommend_similar(df, [
        row["Environment Risk Score"],
        row["Social Risk Score"],
        row["Governance Risk Score"]
    ]))
