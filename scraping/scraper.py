import requests
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp
from flask import current_app

def scrape_article(url: str) -> str:
    """
    Scrapes article text from a URL using Firecrawl.
    Falls back to requests + BeautifulSoup if needed.
    """

    api_key = current_app.config.get("FIRECRAWL_API_KEY")

    # --- Firecrawl primary ---
    if api_key:
        try:
            app = FirecrawlApp(api_key=api_key)
            result = app.scrape_url(
                url,
                params={"formats": ["markdown"]}
            )

            if result and "markdown" in result:
                return result["markdown"].strip()
        except Exception:
            pass  # Silent fallback

    # --- Fallback scraping ---
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        return text.strip()
    except Exception:
        return ""
