import os

from flask import Flask, request, jsonify, Response
import PerAsinScraper
import selectorlib

app = Flask(__name__)
extractor = selectorlib.Extractor.from_yaml_file('selectors.yml')
KEY = 'YOUR_KEY_HERE'


@app.route('/getreviews', methods=['POST'])
def api():
    try:
        asin = request.args.get('asin', None)
        key = request.headers.get('key')

        if asin is None or key is None:
            return None

        if key != KEY:
            return Response("Not authorized", status=403)

        print('url ' + asin + 'key ' + key)
        scraper = PerAsinScraper.PerAsinScraper()
        resp = scraper.scrape_step1("https://www.amazon.com/s?k=" + asin, asin)
        return Response(resp, status=200)

    except Exception as e:
        return Response(e, status=500)


@app.route('/getreviewsummary', methods=['POST'])
def review_summary():
    try:
        asin = request.args.get('asin', None)
        key = request.headers.get('key')

        if asin is None or key is None:
            return None

        if key != KEY:
            return Response("Not authorized", status=403)

        scraper = PerAsinScraper.PerAsinScraper()
        resp = scraper.get_summary_only("https://www.amazon.com/s?k=" + asin, asin)
        return Response(resp, status=200)
    except Exception as e:
        return Response(e, status=500)
