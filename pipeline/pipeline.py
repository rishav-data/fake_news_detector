from model.bert_classifier import classify_text
from scoring.category_score import category_score


def analyze_article_text(article_text: str) -> dict:
    """
    Receives raw article text,
    sends to BERT,
    sends BERT output to category scorer,
    returns structured result.
    """

    # Step 1: BERT classification
    category = classify_text(article_text)

    # Step 2: Category scoring
    cat_score = category_score(category)

    return {
        "category": category,
        "category_score": cat_score
    }
