The main script is PerAsinScraper.py which does all the heavy lifting. main.py is the hook to the scraper. I used flask to host the api and test you can run the scraper stand-alone in way you want.

The inspiration for this is scrapehero.com. I have extened the script to loop over hundreds and potentially thousands of reviews. Be careful though, if you are downloading thousands of reviews for a product then you may need to introduce threading or add sleep between subsequent calls. Ideally you would sleep for 20 secs between each call to avoid being identified as a robot. Thank you RockitSeller (https://www.rockitseller.com) for validating this script.

The script here is for demo/education purpose only and is provided as a starter. What you make of it is your business. 
