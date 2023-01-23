import requests
import random
import time
import json
from lxml import html
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
from selenium import webdriver

# create a logging file
logging.basicConfig(filename='logging.txt', level=logging.ERROR)

# Start with the initial URL
base_url = 'https://example.com/page/'

# Open the file containing the headers
with open('headers.json') as f:
    headers = json.load(f)
    headers_random = random.choice(headers)

# Selenium setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--remote-debugging-port=9222')

# create a new instance of chrome in headless mode
browser = webdriver.Chrome('/home/kwgatheru/Downloads/chromedriver', chrome_options=options)

for i in tqdm(range(2, 3)):
    url = base_url + str(i) + '/'
    # Make a request to the URL
    attempt = 0
    while attempt < 5:
        try:
            browser.get(url)
            response = browser.page_source
            break
        except requests.exceptions.RequestException as e:
            attempt += 1
            logging.error("Network Error: ", e)
            sleep_time = random.randint(1, 10)
            time.sleep(sleep_time)
    else:
        logging.error("Failed to connect after 5 attempts")
        continue
    # Parse the HTML content
    soup = BeautifulSoup(response, 'lxml')
    # Find all the links on the page
    links = soup.find_all('div', {'class':'content-sidebar-wrap'})
    for link in links:
        for el in link.find_all('main', {'class' : 'content'}):
            for l in el.find_all('article'):
                for el_01 in l.find_all('h2', {'class' : 'entry-title'}):

                    print(el_01)

browser.quit()
