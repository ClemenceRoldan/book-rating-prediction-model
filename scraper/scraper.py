## Kheirie : scraper in progress - need to try it on full DF

import requests
from bs4 import BeautifulSoup
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import yaml

def connect_driver(login_url: str): 
    
    """Function to connect to chrome drive; This will be used to get specific stats of specific book editions
    Note that chromedriver.exe needs to be downloaded and found on machine
    
    Args:
        login_url (str): the url where the username and password are entered to login to goodreads
    Returns: 
        the driver object
    """
    chrome_driver_path = ChromeDriverManager().install() # searches for the chromedriver path and installs it

    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
    options.page_load_strategy = "none"

    # Create a Service object with the path to ChromeDriver
    service = Service(chrome_driver_path)

    # Pass the Service object when initializing the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)
 
    driver.get(login_url)
    
    return driver


def get_EditionReview(book_id: int, creds_path: str, login_url: str): 
    
    """Function to get the average review of a specific book edition

    Args:
        book_id (int): id of the book
        creds_path (str): path to yaml file that contain the credentials to login
        login_url (str): the url where the username and password are entered to login to goodreads

    Returns:
        float: average rating 
    """
    
    with open(creds_path, "r") as file:
        credentials = yaml.safe_load(file)
        
    
    driver = connect_driver(login_url)
    
    username = credentials["username"]
    password = credentials["password"]
    log_email = driver.find_element(By.ID, value="ap_email")
    log_pass = driver.find_element(By.ID, value="ap_password")
    log_email.send_keys(username)
    log_pass.send_keys(password)
    log_pass.submit()
    
    stats_url = f"https://www.goodreads.com/book/stats?id={book_id}&just_this_edition=yep"
    driver.get(stats_url)
    
    avgRating = driver.find_element(By.CLASS_NAME, value="infoBoxRowItem.avgRating")
    avgRating = avgRating.text.strip()
    
    driver.quit()
    
    return float(avgRating)


def get_ShelvesAdded(book_id: int, creds_path: str, login_url: str) -> str: 
    
    """Function to get the total number shelves added for a specific book edition

    Args:
        book_id (int): id of the book
        creds_path (str): path to yaml file that contain the credentials to login
        login_url (str): the url where the username and password are entered to login to goodreads

    Returns:
        int: number of shelves the book was added to
    """
    with open("credentials.yaml", "r") as file:
        credentials = yaml.safe_load(file)
        
    
    driver = connect_driver(login_url)
    
    username = credentials["username"]
    password = credentials["password"]
    log_email = driver.find_element(By.ID, value="ap_email")
    log_pass = driver.find_element(By.ID, value="ap_password")
    log_email.send_keys(username)
    log_pass.send_keys(password)
    log_pass.submit()
    
    stats_url = f"https://www.goodreads.com/book/stats?id={book_id}&just_this_edition=yep"
    driver.get(stats_url)
    
    added_to_shelves = driver.find_element(By.XPATH, '//div[@class="infoBoxRowTitle" and text()="Added to shelves"]/following-sibling::div[@class="infoBoxRowItem"]')
    added_to_shelves.text
    
    driver.quit()
    
    return int(added_to_shelves)
    

def get_publisher(book_id: int): 
    """Function to get the publisher of a specific book

    Args:
        book_id (int): id of the book

    Returns:
        str: publisher
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

def get_pagesFormat(book_id: int): 
    """Function to get the format of a specific book (e.g. Paperback, CD, Hardcover etc.)

    Args:
        book_id (int): id of the book

    Returns:
        str: book format
    """
    base_url = f"https://www.goodreads.com/book/show/{book_id}" # the url of the specific book

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    featured_details = soup.find('div', class_='FeaturedDetails')

    pagesFormat = featured_details.find('p', {'data-testid': 'pagesFormat'}).text.split(',')[-1].strip()

    return pagesFormat

def get_firstPublished(book_id: int): 
    """Function to get the first time the book was published (should be the same for all editions)

    Args:
        book_id (int): id of the book

    Returns:
        str: firstPublished, the date of when the book was first published
    """
    base_url = f"https://www.goodreads.com/book/show/{book_id}" # the url of the specific book

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    featured_details = soup.find('div', class_='FeaturedDetails')

    firstPublished = featured_details.find('p', {'data-testid': 'publicationInfo'}).text.strip("First published ")

    return firstPublished


