def final_verdict(
    category_score: int,
    publisher_score: int,
    external_score: int
) -> str:
    """
    Generates final verdict label based on total score (out of 30).
    """

    total = category_score + publisher_score + external_score

    if total >= 22:
        return "High credibility"
    elif total >= 14:
        return "Possibly credible"
    elif total >= 8:
        return "Needs further verification"
    else:
        return "Credibility uncertain"
