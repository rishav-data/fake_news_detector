def final_verdict(category_score: int, publisher_score: int) -> str:
    """
    Generates final verdict label based on total score.
    """

    total = category_score + publisher_score

    if total >= 15:
        return "Possible high credibility"
    elif total >= 7:
        return "Needs further verification"
    else:
        return "Credibility uncertain"