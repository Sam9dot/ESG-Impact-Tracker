def update_esg(base, news_results):
    weights = {"E": 0.4, "S": 0.3, "G": 0.3}
    updated = base.copy()

    for r in news_results:
        impact = r["score"]
        if r["sentiment"] == "NEGATIVE":
            impact *= -1
        updated[r["category"]] += impact * weights[r["category"]]

    updated["ESG"] = updated["E"] + updated["S"] + updated["G"]
    return updated
