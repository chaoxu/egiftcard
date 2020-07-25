import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
import sys

from urllib.parse import urlparse, parse_qs

def html_to_card(html):
  soup = BeautifulSoup(html , 'html.parser')
  title = soup.find("title").get_text().strip()
  vendor = ' '.join(title.split()[1:-2])

  if vendor == 'eBay':
    amount = soup.find("p", {"id": "amount"}).get_text().strip()
    code = soup.find("div", {"class": "cardNum"}).find("span").get_text()
    pin = ''
  if vendor == 'Best Buy':
    z = soup.find("div", {"class": "cardInfo"}).find("div", {"class": "headingText"}).get_text().split()
    amount = z
    for x in z:
      if x[0]=='$':
        amount = x
    code = ''.join(soup.find("span", {"id": "cardNumber2"}).get_text().split())
    pin = soup.find("span", {"id": "Span2"}).get_text()
  return vendor, amount, code, pin

def chrome_get_card(url, raw=False):
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  wb = webdriver.Chrome(options=chrome_options)

  with wb as driver:
    # Set timeout time 
    wait = WebDriverWait(driver, 10)
    # retrive url in headless browser
    driver.get(url)
    
    wait.until(presence_of_element_located((By.CLASS_NAME, "showCard")))
    html = driver.page_source
    driver.close()
    return html_to_card(html)

def get_card(link, raw=False):
  parsed_url = urlparse(link)

  if 'amazon' in parsed_url.netloc:
    bby_url = parse_qs(parsed_url.query)['U'][0]
    return chrome_get_card(bby_url)
  else:
    s = requests.Session()
    #headers = {'User-Agent': USER_AGENT}
    r = s.get(link)
    if raw:
      return r.content
    else:
      return html_to_card(r.content)