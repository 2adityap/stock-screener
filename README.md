# Stock Screener

A program that analyzes stocks based on fundamentals, analyst ratings and "buzz", using Python primarily.

This is done by calling Stock API's and assessing the strength of a company's fundamentals, scraping rating off Yahoo Finance using the Beautiful Soup, and analyzing Tweets about the company at hand using sentiment analysis and the Natural Language Toolkit to determine the overall direction/excitement about the company.

To run:

1) Clone repository, Create environment using `pipenv install` (enter enviornment using `pipenv shell`).
2) Get API Keys from Twitter and Alpha Advantage, and store in local file.
    * This can be done by creating shell script with export statemnts (e.g `export set CONSUMER_KEY='CONSUMER_KEY'`, replacing `'CONSUMER_KEY'` with the actual value)
    * Then source shell script in your environment using `source PATH`, where `PATH` is path to the shell script
3) Run main file `python investing.py`

