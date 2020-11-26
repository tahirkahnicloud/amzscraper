import json
import sys
from random import choice
from time import sleep

import requests
from selectorlib import Extractor


def get_random_user_agent():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
    return choice(user_agent_list)


class PerAsinScraper:
    url = ''
    number_of_reviews = ''
    asin = ''
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_user_agent(),
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    def get_summary_only(self, url, asin):
        self.url = url
        self.asin = asin

        r = requests.get(url, headers=self.headers)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
            return None

        # Pass the HTML of the page and create
        e = Extractor.from_yaml_file('search_results.yml')
        text = e.extract(r.text)
        # step1 completed
        if text is None or text['products'] is None:
            return
        ret_dict = {"reviews": []}
        review = {'title': text['products'][0]['title'], 'url': text['products'][0]['url'],
                  'rating': text['products'][0]['rating'], 'reviews': text['products'][0]['reviews'],
                  'price': text['products'][0]['price']}
        ret_dict['reviews'].append(review)

        return json.dumps(ret_dict)



    def scrape_step1(self, url, asin):
        # step1 start
        self.url = url
        self.asin = asin

        # Download the page using requests
        print("Downloading %s" % self.url)

        r = requests.get(url, headers=self.headers)
        # Simple check to check if page was blocked (Usually 503)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
            return None
        # Pass the HTML of the page and create
        e = Extractor.from_yaml_file('search_results.yml')
        text = e.extract(r.text)
        # step1 completed
        if text is None or text['products'] is None:
            return
        urlsubstring = text['products'][0]['url'].index('ref', 0)
        self.number_of_reviews = text['products'][0]['reviews']
        callUrl = 'https://www.amazon.com' + text['products'][0]['url'][0:urlsubstring - 1]
        resp = self.scrape_step2(callUrl)
        return resp

    def scrape_step2(self, callUrl):
        # Download the page using requests
        print("Downloading %s" % callUrl)
        r = requests.get(callUrl, headers=self.headers)
        # Simple check to check if page was blocked (Usually 503)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n" % callUrl)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d" % (callUrl, r.status_code))
            return None
        # Pass the HTML of the page and create
        e = Extractor.from_yaml_file('selectors.yml')
        text = e.extract(r.text)
        return self.download_reviews(text)

    def download_reviews(self, text):
        urllist = self.get_link_to_all_reviews()

        reviews_dict = {'reviews': []}

        if urllist is None:
            return

        for url in urllist:
            r = requests.get(url, headers=self.headers)
            # Simple check to check if page was blocked (Usually 503)
            if r.status_code > 500:
                if "To discuss automated access to Amazon data please contact" in r.text:
                    print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
                else:
                    print(
                        "Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
                return None
            # Pass the HTML of the page and create
            e = Extractor.from_yaml_file('reviews.yml')
            data = e.extract(r.text)

            if data:
                if data['reviews'] is None:
                    continue

                for row in data['reviews']:
                    review = {'title': row['title'], 'content': row['content'], 'date': row['date'],
                              'variant': row['variant']}
                    if row['images']:
                        image_dict = {'images': []}
                        for i in row['images']:
                            image = {'image': i}
                            image_dict['images'].append(image)
                        review['images'] = image_dict

                    if row['verified'] is not None:
                        review['verified'] = 'Yes'
                    else:
                        review['verified'] = 'No'
                    review['author'] = row['author']
                    review['rating'] = row['rating'].split(' out of')[0]
                    reviews_dict["reviews"].append(review)
            sleep(5)
        return json.dumps(reviews_dict)

    def get_link_to_all_reviews(self):
        if self.number_of_reviews is None or self.number_of_reviews == '':
            return

        self.number_of_reviews = self.number_of_reviews.replace(",", "")
        urllist = []
        number_page_reviews = int(int(self.number_of_reviews) / 10)
        if number_page_reviews % 2 == 0:
            number_page_reviews += 1
        else:
            number_page_reviews += 2

        ind = self.url.index('=', 0)
        asin = self.url[ind + 1:len(self.url)]
        for page_number in range(1, number_page_reviews):
            amazon_url = 'https://www.amazon.com/product-reviews/' + \
                         asin + \
                         '/ref=cm_cr_arp_d_paging_btm_next_' + \
                         str(page_number) + \
                         '?pageNumber=' + \
                         str(page_number)
            urllist.append(amazon_url)

        return urllist


if __name__ == '__main__':
    asin = sys.argv[1]
    if asin is None:
        exit(-1)

    parser = PerAsinScraper()
    parser.scrape_step1("https://www.amazon.com/s?k=" + asin, asin)
