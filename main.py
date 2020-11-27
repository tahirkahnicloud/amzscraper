import json
import os

from flask import Flask, request, jsonify, Response
import PerAsinScraper
import selectorlib

app = Flask(__name__)
extractor = selectorlib.Extractor.from_yaml_file('selectors.yml')
KEY = '3yTh0n!st@'


@app.route('/get_review_details', methods=['POST'])
def review_details():
    try:

        asin = request.args.get('asin', None)
        key = request.headers.get('key')

        if asin is None or key is None:
            return None

        if key != KEY:
            return Response("Not authorized", status=403)

        # get summary
        summary = get_summary()

        scraper = PerAsinScraper.PerAsinScraper()
        resp = scraper.scrape_step1("https://www.amazon.com/s?k=" + asin, asin)

        if resp is None:
            return Response("", status=203)

        summary['products'][0]['product_reviews'] = resp
        return Response(json.dumps(resp), status=200)

    except Exception as e:
        return Response(e, status=500)


@app.route('/get_review_summary', methods=['POST'])
def review_summary():
    try:
        resp = get_summary()
        if resp is None:
            return Response("", status=203)

        return Response(json.dumps(resp), status=200)
        #asin = request.args.get('asin', None)
        #key = request.headers.get('key')

        #if asin is None or key is None:
        #    return None

        #if key != KEY:
        #    return Response("Not authorized", status=403)

        #scraper = PerAsinScraper.PerAsinScraper()
        #resp = scraper.get_summary_only("https://www.amazon.com/s?k=" + asin, asin)
        #return Response(json.dumps(resp), status=200)
    except Exception as e:
        return Response(e, status=500)


def get_summary():
    asin = request.args.get('asin', None)
    key = request.headers.get('key')

    if asin is None or key is None:
        return None

    if key != KEY:
        return Response("Not authorized", status=403)
    scraper = PerAsinScraper.PerAsinScraper()
    return scraper.get_summary_only("https://www.amazon.com/s?k=" + asin, asin)