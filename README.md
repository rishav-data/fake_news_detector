# Fake News Detection System 📰🤖

A hackathon project that analyzes online news articles to estimate their credibility using
Natural Language Processing (NLP) and source-based scoring.

The system combines **content analysis using BERT** with **publisher credibility scoring**
to produce an explainable final verdict.

---

## 🚀 Features

- 🔍 Accepts **news article URLs** or **raw pasted text**
- 🧠 Uses **BERT-based NLP classification** to analyze article tone
- 🏢 Incorporates **publisher credibility scoring** via a curated database
- 🧮 Transparent, rule-based **final scoring logic**
- 🌐 Simple **Flask web interface**
- 🔐 Privacy-first: **no user data or article content is stored**

---

## 🧠 How It Works

1. **Input**
   - User submits an article URL or pastes article text

2. **Article Extraction**
   - URLs are scraped using Firecrawl (with BeautifulSoup fallback)
   - Extracted text is processed in memory only

3. **Content Classification (BERT)**
   - The article is classified into one of:
     - `Neutral`
     - `Biased`
     - `Contradictory`

4. **Scoring**
   - Category Score:
     - Neutral → 10
     - Biased → 5
     - Contradictory → 0
   - Publisher Score:
     - Retrieved from Supabase (0–10)
     - Defaults to 0 if publisher is unknown

5. **Final Verdict**
   - Total Score = Category Score + Publisher Score
   - Verdict thresholds:
     - High score → Possible high credibility
     - Medium score → Needs further verification
     - Low score → Credibility uncertain

---

## 🧰 Tech Stack

### Backend
- Python 3
- Flask

### Machine Learning / NLP
- BERT (HuggingFace Transformers)
- PyTorch
- Scikit-learn (training & evaluation)

### Web Scraping
- Firecrawl
- Requests + BeautifulSoup (fallback)

### Database
- Supabase (PostgreSQL)
  - Stores **only publisher credibility scores**
  - No articles, no user data

### Frontend
- HTML + CSS (Flask templates)

---


---

## 🧪 Model Training

Trained model files are **not included** in this repository.

To train the model locally:
run python model/train_bert.py

This will generate model artifacts inside:

model/bert_news_model/

## 🔐 Privacy & Ethics

No scraped articles are stored

No user data is logged

Publisher scores are manually curated

Final verdicts are advisory, not absolute

This project is intended for educational and research purposes.

🏁 Hackathon Notes

Designed for explainability, not black-box predictions

Modular architecture allows easy upgrades

Can be extended with:

Claim-level fact checking

Multilingual support

Social media misinformation detection

BUILT BY Bhartya Coding Party
Hackathon project – 2026
