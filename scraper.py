## Kheirie : scraper in progress

import requests
from bs4 import BeautifulSoup
import json
import re

def get_publisher(book_id: int) -> str: 
    """
    """
    base_url = f"https://www.goodreads.com/book/show/{book_id}" # the url of the specific book

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    script_tag = soup.find('script', id='__NEXT_DATA__')
    script_content = script_tag.string

    json_content = json.loads(script_content)

    # Find the dynamic key, since the key that homds publisher info changes from book to book in json file
    pattern = re.compile(r'^Book:kca://book/amzn1.gr.book.v1') # the pattern of the key that holds the publisher information
    dynamic_key = next((key for key in json_content.get("props", {}).get("pageProps", {}).get("apolloState", {}) if pattern.match(key)), None)

    # get the publisher
    details = json_content.get("props", {}).get("pageProps", {}).get("apolloState", {}).get(dynamic_key, {}).get("details", {})
    publisher = details.get("publisher", "")

    return publisher

def get_pagesFormat(book_id: int) -> str: 
    """
    """
    base_url = f"https://www.goodreads.com/book/show/{book_id}" # the url of the specific book

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    featured_details = soup.find('div', class_='FeaturedDetails')

    pagesFormat = featured_details.find('p', {'data-testid': 'pagesFormat'}).text.split(',')[-1].strip()

    return pagesFormat

def get_firstPublished(book_id: int) -> str: 
    """
    """
    base_url = f"https://www.goodreads.com/book/show/{book_id}" # the url of the specific book

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    featured_details = soup.find('div', class_='FeaturedDetails')

    firstPublished = featured_details.find('p', {'data-testid': 'publicationInfo'}).text.strip("First published ")

    return firstPublished


