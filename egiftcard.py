import requests
from bs4 import BeautifulSoup

def get_card(link, raw=False):
  s = requests.Session()
  #headers = {'User-Agent': USER_AGENT}
  r = s.get(link)

  soup = BeautifulSoup(r.content , 'html.parser')
  title = soup.find("title").get_text().strip()
  vendor = ' '.join(title.split()[1:-2])
  amount = soup.find("p", {"id": "amount"}).get_text().strip()
  code = soup.find("div", {"class": "cardNum"}).find("span").get_text()
  return vendor, amount, code
