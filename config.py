import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))

    # Firecrawl
    FIRECRAWL_API_KEY = os.getenv("put firecrawl api here")

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # Model
    BERT_MODEL_NAME = os.getenv(
        "BERT_MODEL_NAME",
        "distilbert-base-uncased-finetuned-sst-2-english"
    )
