def category_score(category: str) -> int:
    """
    Maps model category → numeric score.
    """

    mapping = {
        "Neutral": 10,
        "Biased": 5,
        "Contradictory": 0
    }

    return mapping.get(category, 0)
