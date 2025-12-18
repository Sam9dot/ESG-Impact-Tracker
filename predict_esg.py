import pickle
from preprocess import clean_text

model = pickle.load(open("models/esg_classifier.pkl", "rb"))
vectorizer = pickle.load(open("models/tfidf.pkl", "rb"))

def predict_category(text):
    X = vectorizer.transform([clean_text(text)])
    return model.predict(X)[0]
