from supabase import create_client
from flask import current_app

_supabase = None

def get_supabase():
    global _supabase

    if _supabase is None:
        url = current_app.config.get("SUPABASE_URL")
        key = current_app.config.get("SUPABASE_KEY")

        if not url or not key:
            raise RuntimeError("Supabase credentials not configured")

        _supabase = create_client(url, key)

    return _supabase
