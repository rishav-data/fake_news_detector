from transformers import pipeline
from flask import current_app
from utils.text_cleaner import clean_text

_classifier = None

def load_model():
    global _classifier
    if _classifier is None:
        model_name = current_app.config["BERT_MODEL_NAME"]
        _classifier = pipeline(
            "text-classification",
            model=model_name,
            return_all_scores=True
        )
    return _classifier


def classify_text(text: str) -> str:
    """
    Returns: Neutral | Biased | Contradictory
    """

    classifier = load_model()
    cleaned = clean_text(text)[:512]  # hard cap for safety

    scores = classifier(cleaned)[0]

    # Example mapping logic (can be swapped with your fine-tuned model)
    top = max(scores, key=lambda x: x["score"])

    label = top["label"].lower()

    if "neutral" in label:
        return "Neutral"
    elif "negative" in label:
        return "Contradictory"
    else:
        return "Biased"
