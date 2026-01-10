import re

def clean_text(text: str) -> str:
    """
    Basic normalization before inference.
    """

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z0-9.,!? ]", "", text)

    return text.strip()
