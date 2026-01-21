#import
from flask import Flask, request, jsonify, render_template
from config import Config

# Core pipeline imports
from scraping.article_reader import read_article
from model.bert_classifier import classify_text
from scoring.category_score import category_score
from scoring.publisher_score import get_publisher_score
from scoring.verdict import final_verdict
from utils.publisher_normalizer import normalize_publisher
from utils.external_validator import external_validation_score


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # -------------------------
    # UI PAGE ROUTES (GET)
    # -------------------------

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/article-text", methods=["GET"])
    def article_text_page():
        return render_template("article_text.html")

    @app.route("/article-link", methods=["GET"])
    def article_link_page():
        return render_template("article_link.html")

    # -------------------------
    # ANALYZE ROUTE (POST)
    # -------------------------

    @app.route("/analyze", methods=["POST"])
    def analyze():
        try:
            # Accept input from either form
            raw_input = (
                request.form.get("article_text")
                or request.form.get("article_url")
            )

            if not raw_input:
                return jsonify({"error": "Missing input"}), 400

            # Read article (URL or raw text)
            article_text, source_url = read_article(raw_input)

            if not article_text:
                return jsonify({"error": "Unable to extract article text"}), 400

            # -------------------------
            # BERT CLASSIFICATION
            # -------------------------
            category = classify_text(article_text)
            cat_score = category_score(category)

            # -------------------------
            # PUBLISHER SCORE
            # -------------------------
            publisher_raw = request.form.get("publisher")
            try:
                publisher = normalize_publisher(publisher_raw) if publisher_raw else None
            except Exception:
                publisher = None

            pub_score = get_publisher_score(publisher)

            # -------------------------
            # EXTERNAL VALIDATION SCORE
            # -------------------------
            external_score = external_validation_score(article_text)

            # -------------------------
            # FINAL VERDICT (OUT OF 30)
            # -------------------------
            verdict = final_verdict(
                cat_score,
                pub_score,
                external_score
            )

            total_score = cat_score + pub_score + external_score

            # ✅ ALWAYS RETURN
            return render_template(
                "result.html",
                category=category,
                category_score=cat_score,
                publisher=publisher or "Unknown",
                publisher_score=pub_score,
                external_score=external_score,
                final_score=total_score,
                verdict=verdict
            )

        except Exception as e:
            # Absolute fallback (never let Flask return None)
            return jsonify({
                "error": "Internal processing error",
                "details": str(e)
            }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=app.config["PORT"],
        debug=True,
        use_reloader=False
    )
