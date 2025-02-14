import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.sunat.gob.pe"

driver.get(url)

soup = BeautifulSoup(driver.page_source, features= 'lxml')

fields = soup.find_all(name='li', attrs={'class': 'flex'})
for field in fields:
    print(field.getText())

time.sleep(10)

driver.quit()

