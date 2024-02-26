import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import yaml
import polling2, time
import random
import numpy as np
from os.path import exists 
import pandas as pd

driver = None
DEBUG = True

def myprint(*args, **kwargs):
    """this function is used to control printing througout the code
        if DEBUG is set to True then print, if False then do not print
    """
    
    global DEBUG 
    if DEBUG: # if false does not print
        print(*args, **kwargs)

def connect_driver(): 
    """function to connect to driver, in our case Chrome driver
    """
    
    global driver

    myprint("Setting Driver ...> ", end='')
 
    driver = uc.Chrome(headless=True,use_subprocess=False, version_main = 120)
    
    myprint('OK')
    
def driver_quit():
    """function to quit the driver
    """
    driver.quit()

def getPage(url, timeout=8):
    """function to load a specific page (url)

    Args:
        url (str): the url of the page to connect to
        timeout (int): time in seconds to wait for a page to load before throwing an error. Defaults to 8.

    Returns:
        bool: True if page load is successful else False
    """
    myprint('Getting Page :', url, ' ...> ', end='')
    
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        page_source = driver.page_source
        
        if not page_source:
            print("Page empty")
            return False
        
        myprint('OK')
        return True
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def is_logged_in():
    """function to check if the login to website was successful

    Returns:
        bool: True if login is successful else False
    """
    if driver.get_cookie('sess-at-main') == None:
        return False
    return True

def login(creds_path='../private/credentials.yaml'):
    """function to login to a specific website

    Args:
        creds_path (str): yaml file that holds the credentials "username: USERNAME" and "password: PASSWORD"

    Returns:
        int: 1 is login is successful, 0 if login failed, -1 incase of exception
    """
    
    global driver
    login_url = r"https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=8ee875637040e51dac0713257c042f88"
    
    try:
        val = getPage(login_url)
        
        if not val: 
            # was not able to get page
            return 0
        
        myprint('Getting login credentials from config file:', creds_path, ' ...> ', end='')
        with open(creds_path, "r") as file:
            credentials = yaml.safe_load(file)
            username = credentials["username"]
            password = credentials["password"]
            myprint('OK')
        
        myprint('Setting credentials in login page form ...> ', end='')
        log_email = polling2.poll(lambda: driver.find_element(By.ID, value="ap_email"), step=4, timeout=10)
        log_email.send_keys(username)
        log_pass = polling2.poll(lambda: driver.find_element(By.ID, value="ap_password"), step=3, timeout=10)
        log_pass.send_keys(password)
        log_pass.submit()
        myprint('OK')
        myprint('Connecting to goodreads ...> ', end='')

        time.sleep(random.uniform(2, 6))

        if is_logged_in():
            myprint(driver.current_url, ' ...> OK')
            return 1
        else:
            myprint('Loggin Failed')
            return 0
            
    except Exception as e:
        myprint(f"Error occurred: {e}")
        return -1

def get_avgRating_shelvesAdded(book_id):
    """function to get the average rating and added to shelves of a specific book edition

    Args:
        book_id (int): the id of the book

    Returns:
        dict: dictionary that stores the values of the average rating (avg_rating) and added to shelves (added_to_shelves) of the book
    """
    
    url = f"https://www.goodreads.com/book/stats?id={book_id}&just_this_edition=yep"
    myprint('Getting AvgRating & ShelvesAdded :')
    
    # connect to page
    time.sleep(random.uniform(2, 8))
    val = getPage(url)
    
    # if connection to page fails
    if not val:
        myprint(f"Connecting to {url} failed !!! \n try to connect again ...")
        
        # disconnect then connect again
        driver_quit()
        time.sleep(random.uniform(30, 60))
        
        connect_driver()
        login()
        
        val = getPage(url)
        
        if not val: 
            myprint(f"!!!!! Failed to connect to {url} saving values as nan !!!!!")
            return dict({
                'avg_rating' : np.nan,
                'added_to_shelves' : np.nan
            })
        
    
    myprint('---> AvgRating : ', end='')
    
    try: # trying getting the average rate
        avg_rating = polling2.poll(lambda: driver.find_element(By.CLASS_NAME, value="infoBoxRowItem.avgRating"), step=6, timeout=15)
        avg_rating = avg_rating.text.strip()
        avg_rating = float(avg_rating)
        myprint(avg_rating)
    except Exception as e: # incacse of exception set avg_rating to np.nan
        myprint(f"!!!!! Could not get the average ratings due to the following exception: {e} !!!!!")
        myprint("!!!!! avg_rating will be set to nan !!!!!")
        avg_rating = np.nan
    
    myprint('---> ShelvesAdded : ', end='')
    
    try: # trying to get added_to_shelves
        added_to_shelves = polling2.poll(lambda: driver.find_element(By.XPATH, '//div[@class="infoBoxRowTitle" and text()="Added to shelves"]/following-sibling::div[@class="infoBoxRowItem"]'), step=8, timeout=15)
        added_to_shelves = added_to_shelves.text.strip().replace(',','')
        added_to_shelves = int(added_to_shelves)
        myprint(added_to_shelves)
    except Exception as e: # incase of exception set added_to_shelves to np.nan
        myprint(f"!!!!! Could not get added to shelves due to the following exception: {e} !!!!!")
        myprint("!!!!! added_to_shelves will be set to nan !!!!!")
        added_to_shelves = np.nan
    
    return dict({
        'avg_rating' : avg_rating,
        'added_to_shelves' : added_to_shelves
    })


def get_publisher():
    """function to get the publisher of a specific book

    Returns:
        str|np.nan: a string representing the publisher or np.nan incase getting the publisher failed
    """
    
    try:
        script_element = polling2.poll(lambda: driver.find_element(By.ID,"__NEXT_DATA__"), step=4, timeout=10)
        script_content = script_element.get_attribute("innerHTML")
        json_content = json.loads(script_content)
    
    
        # Find the dynamic key, since the key that homds publisher info changes from book to book in json file
        pattern = re.compile(r'^Book:kca://book/amzn1.gr.book.v1') # the pattern of the key that holds the publisher information
        dynamic_key = next((key for key in json_content.get("props", {}).get("pageProps", {}).get("apolloState", {}) if pattern.match(key)), None)

        # get the publisher
        details = json_content.get("props", {}).get("pageProps", {}).get("apolloState", {}).get(dynamic_key, {}).get("details", {})
        publisher = details.get("publisher", "")
    except Exception as e:

        myprint(f"!!!!! Could not get publisher due to the following exception: {e} !!!!!")
        myprint("!!!!! publisher will be set to nan !!!!!")
        publisher = np.nan      
   
    return publisher


def get_pagesFormat():
    """function to get the pages format of a book (e.g. paperback, hardcover, CD, ebook etc.)

    Returns:
        str|np.nan: a string representing the pages format or np.nan incase getting the pages format failed
    """
    
    try:
        pagesFormat = polling2.poll(lambda: driver.find_element(By.XPATH, '//p[@data-testid="pagesFormat"]'), step=7, timeout=12)
        pagesFormat = pagesFormat.text.split(',')[-1].strip()
    except Exception as e: 
        myprint(f"!!!!! Could not get page format due to the following exception: {e} !!!!!")
        myprint("!!!!! pagesFormat will be set to nan !!!!!")
        pagesFormat = np.nan         
    
    return pagesFormat


def get_firstPublished():
    """function to get the first published date of a book

    Returns:
        str|np.nan: a string representing the first published date or np.nan incase getting the first published date failed
    """
    
    try:
        firstPublished = polling2.poll(lambda: driver.find_element(By.XPATH, '//p[@data-testid="publicationInfo"]'), step=5, timeout=13)
        firstPublished = firstPublished.text.strip("First published ")
    except Exception as e: 
        myprint(f"!!!!! Could not get first published due to the following exception: {e} !!!!!")
        myprint("!!!!! firstPublished will be set to nan !!!!!")
        firstPublished = np.nan         
    return firstPublished

def get_publisher_pagesFormat_firstPublished(book_id):
    """function to get the publisher, pages format and first published date of a specific book edition

    Args:
        book_id (int): the id of the book

    Returns:
        dict: dictionary that stores the values of the publisher, pages format (page_format) and first published date (first_published) of the book
    """
    
    url = f"https://www.goodreads.com/book/show/{book_id}"
    myprint('Getting publisher, pageFormat * firstPublished :')
    
    # connect to page
    time.sleep(2)
    val = getPage(url)
    
    # if connection to page fails
    if not val:
        
        print(f"Connecting to {url} failed !!! \n try to connect again ...")
        
        # disconnect then connect again
        driver_quit()
        time.sleep(random.uniform(30, 60))
        
        connect_driver()
        login()
        val = getPage(url)
        
        if not val: 
            print(f"!!!!! Failed to connect to {url} saving values as nan !!!!!")
            return dict({
        'publisher': np.nan,
        'page_format': np.nan,
        'first_published': np.nan
        })
    
    # Getting Publisher
    myprint('---> Publisher : ', end='')
    publisher = get_publisher()
    myprint(publisher)
    
    # Getting PageFormat
    myprint('---> PageFormat : ', end='')
    page_format = get_pagesFormat()
    myprint(page_format)
    
    # Getting PageFormat
    myprint('---> FirstPublished : ', end='')
    first_published = get_firstPublished()
    myprint(first_published)
    
    return dict({
        'publisher': publisher,
        'page_format': page_format,
        'first_published': first_published
    })


def scrape_by_dfIDs(df, start_index=0, batch_size=100, min_throttle_delay=5, max_throttle_delay=10):
    """function to scrape the new features for all book_id in a specific df

    Args:
        df (pd.DataFrame): the pandas DataFrame used to add the new features to, it should have 'bookID' column in it
        start_index (int, optional): the DataFrame index to start scraping from. Defaults to 0.
        batch_size (int, optional): the size of the batch to process. Defaults to 100.
        min_throttle_delay (int, optional): minimum timeout in seconds to wait. Defaults to 5.
        max_throttle_delay (int, optional): maximum timeout in seconds to wait. Defaults to 10.

    Returns:
        pd.DataFrame: the updated df
    """
    # Load the last scraped index if it exists - this file stores the last index reached after apply the scraper. 
    # Important incase of unexpected interruptions
    last_index_file = "last_scraped_index.txt"
    
    # if last_index_file does not exist create a new one
    if exists(last_index_file):
        with open(last_index_file, "r") as file:
            start_index = int(file.read())
    
    # if the new .csv file to store the updated df does not exist, create a new one        
    if not exists("booksRating_extraFeats.csv"):
        df = df.assign(first_published=np.nan,
                   book_format=np.nan,
                   new_publisher=np.nan,
                   edition_avgRating=np.nan,
                   added_toShelves=np.nan)
    
        df.to_csv("booksRating_extraFeats.csv", index=False)
        
    else:
        df = pd.read_csv("booksRating_extraFeats.csv")
    
    print("Started Scraping process from index {start_index} ...")
    
    
    # Iterate over each row in the DataFrame starting from the last scraped index
    for index in range(start_index, len(df), batch_size):
        breaker = False
        
        batch_df = df.iloc[index:index+batch_size]
        
        for batch_index, row in batch_df.iterrows():
            throttle_delay = random.uniform(min_throttle_delay, max_throttle_delay)

            # Save the index of the last scraped row
            with open(last_index_file, "w") as file:
                file.write(str(batch_index))
            
            # make sure it is properly logged in   
            if not is_logged_in:
                
                throttle_delay = random.uniform(min_throttle_delay, max_throttle_delay)
                
                time.sleep(throttle_delay)
                val = login()
                if not val: 
                    driver_quit()
                    connect_driver()
                    val = login()
                    
                    if not val: 
                        print("stopping the process ... Not able to sign in")
                        breaker = True
                        break
                if val == -1: 
                    print("stopping the process ... failed to connect because of unexpected error")
                    breaker = True
                    break
                
            avgR_shelvesA = get_avgRating_shelvesAdded(row['bookID'])
                
            pub_pagesF_firstP = get_publisher_pagesFormat_firstPublished(row['bookID'])
            
            # Append the result to the df
            df.at[batch_index, "first_published"] = pub_pagesF_firstP["first_published"]
            df.at[batch_index, "book_format"] = pub_pagesF_firstP["page_format"]
            df.at[batch_index, "new_publisher"] = pub_pagesF_firstP["publisher"]
            df.at[batch_index, "edition_avgRating"] = avgR_shelvesA["avg_rating"]
            df.at[batch_index, "added_toShelves"] = avgR_shelvesA["added_to_shelves"]
            
            
            
            # update the existing csv file
            df.to_csv("booksRating_extraFeats.csv", index=False)
            
            # Set up delays between requests to avoid overwhelming the server
            throttle_delay = random.uniform(min_throttle_delay, max_throttle_delay)
            time.sleep(throttle_delay)
        
        if breaker: 
            print("!!! process stopped - failed to connect !!!")
            break
        
        print(batch_df.sample(3))        
        
        
        print("Processed", min(index + batch_size, len(df)), "rows")
    
    print("--- Scraping ended ---")
   
    return df