import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
import time

nltk.download("punkt", quiet=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def _first_20_tokens(text: str) -> str:
    tokens = word_tokenize(text)
    return " ".join(tokens[:20])

def _duckduckgo_result_count(query: str) -> int:
    url = "https://html.duckduckgo.com/html/"
    response = requests.post(
        url,
        data={"q": query},
        headers=HEADERS,
        timeout=10
    )

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="result")
    return len(results)

def _score_mapping(count: int) -> int:
    if count == 0:
        return 1
    elif count <= 2:
        return 3
    elif count <= 5:
        return 5
    elif count <= 9:
        return 7
    else:
        return 10

def external_validation_score(article_text: str) -> int:
    """
    Returns external validation score (1–10)
    based on cross-publication presence.
    """
    try:
        query = _first_20_tokens(article_text)
        time.sleep(1)  # polite crawl delay
        count = _duckduckgo_result_count(query)
        return _score_mapping(count)
    except Exception:
        # Fail-safe: neutral-low confidence
        return 1
