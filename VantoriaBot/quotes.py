from bs4 import BeautifulSoup
import requests
#import pandas as pd
import urllib.request
import time

# Lists to store the quote data
quotes = []
authors = []

# Create a function to scrape the website for different genres of quotes
def quote_website_scraper(genre, page_num):

    # get the page number as a string, append page number to url
    pg_num = str(page_num)
    quote_url = f'https://www.goodreads.com/quotes/tag/{genre}?page={pg_num}'
    
    # make a request to access the website
    page = requests.get(quote_url)

    # parse text from website
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # get tag and class
    quoteText = soup.find_all('div', class_='quoteText')
    
    # get all the quotes and authors and append to lists
    for i in quoteText:

        # get the text of the current index quote
        text = i.text.strip().split('\n')[0]
        
        # get the author of the current index quote
        author = i.find('span', class_='authorOrTitle').text.strip()
        author = author.replace(',','') # str.replace()
        
        # add data to arrays
        quotes.append(text)
        authors.append(author)


def final_quote_generator(genre):

    # We want quotes from the first 5 pages of the given genre
    number_of_pages = 5
    for number in range (0, number_of_pages):
        quote_website_scraper(genre, number)

    # Combine lists
    # combine quotes with their corresponding author
    final_quotes = []
    for i in range(len(quotes)):
        final_quotes.append(f'{quotes[i]} -- {authors[i]}')

    return final_quotes

