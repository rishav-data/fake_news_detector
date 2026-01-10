from database.supabase_client import get_supabase

def get_publisher_score(publisher_domain: str | None) -> int:
    """
    Returns publisher credibility score (0–10).
    Defaults to 0 if publisher is unknown or missing.
    """

    if not publisher_domain:
        return 0

    try:
        supabase = get_supabase()
        response = (
            supabase
            .table("publisher_scores")
            .select("credibility_score")
            .eq("publisher_domain", publisher_domain)
            .single()
            .execute()
        )

        data = response.data
        if data and "credibility_score" in data:
            return int(data["credibility_score"])

    except Exception:
        pass

    return 0
