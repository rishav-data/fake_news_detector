import validators
from scraping.scraper import scrape_article

def read_article(user_input: str):
    """
    Determines whether input is a URL or raw text.
    Returns (article_text, source_url)
    """

    if validators.url(user_input):
        text = scrape_article(user_input)
        return text, user_input

    # Assume raw pasted article
    return user_input.strip(), None
