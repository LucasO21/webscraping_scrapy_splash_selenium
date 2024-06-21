# Imports
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service
from lxml import etree


# Headless Option
options = Options()
options.add_argument("--headless")

# Driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.cannondale.com/en-us/bikes")

# Wait
element = WDW(driver, 20).until(EC.presence_of_element_located((
    By.XPATH, '//div[@class="product-card card filter-and-sort__product -has-3Q "]'
)))

# Page HTML
soup = BS(driver.page_source, 'lxml')

# Bike Cards
bike_card = soup.find_all('div', class_='product-card card filter-and-sort__product -has-3Q')


# Bike Hrefs
bike_urls = []
for card in bike_card:
    url = card.find('a')['href']
    full_url = f"https://www.cannondale.com{url}"
    bike_urls.append(full_url)


# Bike Details from Each Bike URL
sample_url = bike_urls[0]

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(sample_url)

# Wait
element = WDW(driver, 20).until(EC.presence_of_element_located((
    By.XPATH, '//h1[@class="headline bike-configuration__headline"]'
)))

def get_bike_details(soup, html, class_):

    try:
        value = soup.find(html, class_=class_)
    except:
        value = np.nan
    return value


# Page HTML
bike_page_soup = BS(driver.page_source, 'lxml')

header = bike_page_soup.find('h1', class_='headline bike-configuration__headline').text.split("\n")
header = [item.strip() for item in header if item.strip() != '']
bike_name = header[0]
bike_model = header[1]

header = get_bike_details(bike_page_soup, 'h1', 'headline bike-configuration__headline').text
bike_name = [item.strip() for item in header.split("\n") if item.strip() != ''][0]
bike_model = [item.strip() for item in header.split("\n") if item.strip() != ''][1]

price = get_bike_details(bike_page_soup, 'div', 'bike-configuration__price').text
color = get_bike_details(bike_page_soup, 'span', 'pdp__color-select color swatch-bpt active')["data-color"]

bike_page_soup.find("li", class_ = "specs-list-item").find("strong", class_ = "name").text

bike_page_soup.find("li", class_ = "specs-list-item")


parent_div = bike_page_soup.find('strong', text='Model Code').parent
model_code_div = parent_div.find('div', class_='desc').text

name = bike_page_soup.find('strong', text='Platform').parent.find("div", class_="desc").text.strip()
model = bike_page_soup.find('strong', text='Model Name').parent.find("div", class_="desc").text.strip().strip(name)
code = bike_page_soup.find('strong', text='Model Code').parent.find("div", class_="desc").text.strip()
frame = bike_page_soup.find('strong', text='Frame').parent.find("div", class_="desc").text.strip()
fork = bike_page_soup.find('strong', text='Fork').parent.find("div", class_="desc").text.strip()


def get_bike_details(soup, text):
    try:
        value = soup.find("strong", string=text).parent.find("div", class_="desc").text.strip()
    except:
        value = np.nan
    return value


name = get_bike_details(bike_page_soup, 'Platform')
model = get_bike_details(bike_page_soup, 'Model Name')
code = get_bike_details(bike_page_soup, 'Model Code')
frame = get_bike_details(bike_page_soup, 'Frame')
form = get_bike_details(bike_page_soup, 'Fork')
headset = get_bike_details(bike_page_soup, 'Headset')
rear_derailleur = get_bike_details(bike_page_soup, 'Rear Derailleur')
front_derailleur = get_bike_details(bike_page_soup, 'Front Derailleur')
shifters = get_bike_details(bike_page_soup, 'Shifters')
chain = get_bike_details(bike_page_soup, 'Chain')
crank = get_bike_details(bike_page_soup, 'Crank')
rear_cogs = get_bike_details(bike_page_soup, 'Rear Cogs')
botton_bracket = get_bike_details(bike_page_soup, 'Bottom Bracket')




bike_features_tags_list = bike_page_soup.find_all("strong", class_="name")
bike_features_text_list = [tag.text for tag in bike_features_tags_list]

df = pd.DataFrame(columns=bike_features_text_list)

for feature in bike_features_text_list:
    value = get_bike_details(bike_page_soup, feature)
    df[feature] = [value]


df