from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch_books():
    data = request.json
    titles = data.get('titles', [])
    source = data.get('source', 'oceanofpdf')

    results = {}

    for title in titles:
        if source == "oceanofpdf":
            search_url = f"https://oceanofpdf.com/?s={title.replace(' ', '+')}"
            html = requests.get(search_url).text
            soup = BeautifulSoup(html, 'html.parser')
            link = soup.select_one('.entry-title a')
            results[title] = link['href'] if link else 'Not found'

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)
