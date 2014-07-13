#
#   Stock Ticker Soup
#   Copyright (c) 2014 Brian Wilcox
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#
#   Stock Ticker Soup scrapes the stock tickers belonging to the S&P500 and
#   generates a csv file of the results
#
#   Contact me at http://brianmwilcox.com
#
from bs4 import BeautifulSoup
import requests
import csv
import re


class StockScraper:
    """
    Class to download, scrape, and save the stock tickers for the S&P500
    """
    def __init__(self, ticker_urls):
        self.url = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self.ticker_urls = ticker_urls
        self.data = None
        self.output = []

    def get_data(self):
        """
        Download the web page data and create a beautiful soup object from it
        Store resulting soup object as a component of this stock scraper object
        """
        r = requests.get(self.url)
        data = r.text
        self.data = BeautifulSoup(data)

    def __scrape_tickers_from_a_url(self, url_to_scrape):
        """
        Find the relevant URLs and strip the stock tickers out of them
        """
        if self.data is not None:
            i = 0
            for n in self.data.find_all('a', href=re.compile(url_to_scrape)):
                n = n.__str__().split('>')
                n = n[1]
                n = n.split('<')
                n = n[0]
                i += 1
                self.output.append(n)
        else:
            raise Exception('Web page data is not instantiated. Exiting now.')

    def scrape_urls(self):
        """
        For dealing with multiple URLs of interest containing text to scrape
        """
        for x in self.ticker_urls:
            self.__scrape_tickers_from_a_url(x)

    def write_stock_tickers_csv(self, csv_file):
        """
        Take resulting stock ticker list, sort it and push it to a csv file
        """
        f = open(csv_file, 'w')
        self.output = sorted(self.output)
        for x in self.output:
            f.write('\"' + x + '\"\n')
        f.close()


def main():
    """
    Create a stock ticker object and pass it the base URLs to look for, parse Wikipedia
    for the stock tickers, sort and save the result as a csv file
    """
    # List of URLs with stock tickers in them up to date as of 07-12-2014
    urls_with_tickers = ['http://www\.nyse\.com/quote/XNYS\:', 'http://www\.nasdaq\.com/symbol/']
    my_scraper = StockScraper(urls_with_tickers)
    my_scraper.get_data()
    my_scraper.scrape_urls()
    my_scraper.write_stock_tickers_csv('sp500.csv')


main()