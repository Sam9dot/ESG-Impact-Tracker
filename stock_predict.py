def predict_stock(yesterday, today):
    return "Likely to Rise 📈" if today["ESG"] > yesterday["ESG"] else "Likely to Fall 📉"
