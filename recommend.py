import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend_similar(df, row):
    features = df[[
        "Environment Risk Score",
        "Social Risk Score",
        "Governance Risk Score"
    ]].values

    features = np.nan_to_num(features)
    row = np.nan_to_num(row)

    sims = cosine_similarity([row], features)[0]
    df["similarity"] = sims

    return df.sort_values("similarity", ascending=False).head(5)
