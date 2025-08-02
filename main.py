from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/fetch", methods=["POST"])
def fetch_books():
    data = request.json
    titles = data.get("titles", [])
    source = data.get("source", "oceanofpdf")
    results = {}

    for title in titles:
        if source == "oceanofpdf":
            url = f"https://oceanofpdf.com/?s={title.replace(' ', '+')}"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            link = soup.select_one('.entry-title a')
            results[title] = link['href'] if link else "Not found"

    return jsonify(results)

@app.route("/", methods=["GET"])
def home():
    return "📚 Research Fetcher is online."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
