from gnews import GNews

def fetch_news(company):
    news = GNews(language="en", max_results=8)
    data = news.get_news(company)
    return [d["title"] + " " + d["description"] for d in data]
