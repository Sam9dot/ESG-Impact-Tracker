import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import clean_text

df = pd.read_csv("data/esg_companies.csv")

texts = df["Description"].apply(clean_text)

def label_row(row):
    scores = {
        "E": row["Environment Risk Score"],
        "S": row["Social Risk Score"],
        "G": row["Governance Risk Score"]
    }
    return max(scores, key=scores.get)

labels = df.apply(label_row, axis=1)

vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=500)
model.fit(X, labels)

pickle.dump(model, open("models/esg_classifier.pkl", "wb"))
pickle.dump(vectorizer, open("models/tfidf.pkl", "wb"))
