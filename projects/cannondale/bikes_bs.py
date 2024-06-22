

# ------------------------------------------------------------------------------
# SETUP ----
# ------------------------------------------------------------------------------

# Libraries ----
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

# Pandas Options ----
pd.set_option('display.max_columns', None)

# ------------------------------------------------------------------------------
# STARTING URL
# ------------------------------------------------------------------------------

# Headless Option ----
options = Options()
options.add_argument("--headless")


# Get Driver ----
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.cannondale.com/en-us/bikes")


# Wait For Elements to Load ----
element = WDW(driver, 20).until(EC.presence_of_element_located((
    By.XPATH, '//div[@class="product-card card filter-and-sort__product -has-3Q "]'
)))

# Get Page HTML ----
soup = BS(driver.page_source, 'lxml')


# Get All Bike Cards ----
bike_card = soup.find_all('div', class_='product-card card filter-and-sort__product -has-3Q')

len(bike_card)


# Extract Image URLs from Each Bike Card ----
bike_image_urls = []
for card in bike_card:
    try:
        img_url = card.find('img')['src']
    except:
        pass

    bike_image_urls.append(img_url)

len(bike_image_urls)


# Bike Hrefs for Each Bike Card ----
bike_detail_urls = []
for card in bike_card:
    try:
        url = card.find('a')['href']
        full_url = f"https://www.cannondale.com{url}"
    except:
        pass

    bike_detail_urls.append(full_url)

len(bike_detail_urls)


# ------------------------------------------------------------------------------
# FUNCTIONS TO GET BIKE DETAILS ----
# ------------------------------------------------------------------------------

# Function to Get Bike Description ----
def get_bike_feature_details(soup, text):
    try:
        value = soup.find("strong", string=text).parent.find("div", class_="desc").text.strip()
    except:
        value = np.nan
    return value

# Function to Get Bike Description 1 ----
def get_bike_description_1(soup):
    try:
        value = soup.find('div', class_ = "highlights thrives-built")
    except:
        value = np.nan

    try:
        heading = value.find("h3").text.strip()
    except:
        heading = ""

    try:
        text = value.find("p").text.strip()
    except:
        text = ""

    full_description = f"{heading} : {text}"

    return full_description

# Function to Get Bike Description 2 ----
def get_bike_description_2(soup):
    try:
        value = soup.find('div', class_ = "highlights thrives-built")
    except:
        value = np.nan

    try:
        heading = value.find_all("h3")[1].text.strip()
    except:
        heading = ""

    try:
        text = value.find_all("p")[1].text.strip()
    except:
        text = ""

    full_description = f"{heading} : {text}"

    return full_description

# Function to Get Bike Description 3 ----
def get_bike_description_3(soup):
    try:
        value = soup.find('div', class_ = "highlights thrives-built")
    except:
        value = np.nan

    try:
        heading = value.find_all("h3")[2].text.strip()
    except:
        heading = ""

    try:
        text = value.find_all("p")[2].text.strip()
    except:
        text = ""

    full_description = f"{heading} : {text}"

    return full_description

# Function to Get Bike Highlights ----
def get_bike_highlights(soup):

    try:
        highlights = soup.select_one('div.highlights:not(.thrives-built)') # using css selector to get the `highlights` div
        li = highlights.find_all('li') # getting all the `li` tags
        li_text_joined = "; ".join([item.text for item in li]) # joining the text of all the `li` tags
    except:
        li_text_joined = np.nan

    return li_text_joined

# Function to Get Price ----
def get_bike_price(soup, sale_price=False):
    try:
        price = soup.find('div', class_='bike-configuration__price').text
    except:
        price = np.nan

    price_list = [price for price in price.split("$") if price]

    if sale_price:
        return price_list[1] if len(price_list) > 1 else np.nan
    else:
        return price_list[0]

# Function to Get Bike Image URL ----
def get_bike_color(soup):
    try:
        color_span = bike_page_soup.find('span', class_=lambda x: x and "pdp__color-select" in x and "color" in x)
        color = color_span['data-color'] if color_span and 'data-color' in color_span.attrs else np.nan
    except:
        color = np.nan

    return color

# Function to Get Bike Image URL ----
def get_bike_image_url(soup):
    try:
        img_url = bike_page_soup.find('picture').find('img')['src']
    except:
        img_url = np.nan

    return img_url

# ------------------------------------------------------------------------------
# EXTACT BIKE DETAILS ----
# ------------------------------------------------------------------------------

# Empty List to Hold Bike Details Dictionaries ----
bike_details_list = []

# Sample URLs for Testing ----
# sample_urls = bike_detail_urls[:5]
# url = bike_detail_urls[26]

start_time = time.time()
print(f"Total Number of Bikes: {len(bike_detail_urls)}")
for index, url in enumerate(bike_detail_urls, start = 1):

    driver = None
    try:
        print("-----------------------------------------")
        print(f"Extracting details for Bike #{index}...")
        start_time_ = time.time()

        # Get Headless Driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        # Wait For Elements to Load
        element = WDW(driver, 20).until(EC.presence_of_element_located((
            By.XPATH, '//h1[@class="headline bike-configuration__headline"]'
        )))

        # Get Page HTML
        bike_page_soup = BS(driver.page_source, 'lxml')

        # Get The Bike Feature Name HTML Tags
        bike_features_tags_list = bike_page_soup.find_all("strong", class_="name")

        # Get The Bike Feature Names
        bike_features_text_list = [tag.text for tag in bike_features_tags_list]

        # Add price, color, description_1, description_2, description_3, highlights to the list
        bike_features_text_list.insert(2, "price")
        bike_features_text_list.insert(3, "sale_price")
        bike_features_text_list.insert(4, "color")
        bike_features_text_list.insert(5, "description_1")
        bike_features_text_list.insert(6, "description_2")
        bike_features_text_list.insert(7, "description_3")
        bike_features_text_list.insert(8, "highlights")
        bike_features_text_list.insert(len(bike_features_text_list), "bike_image_url")

        # Extract All Other Bike Features
        dict_ = {}
        for feature in bike_features_text_list:
            value = get_bike_feature_details(bike_page_soup, feature)
            dict_[feature] = value

        # Get Bike Price. (Price is not in the bike_features_text_list and must be extracted separately)
        price = get_bike_price(bike_page_soup)
        sale_price = get_bike_price(bike_page_soup, sale_price=True)

        # Get Bike Color (Color is not in the bike_features_text_list and must be extracted separately)
        color = get_bike_color(bike_page_soup)

        # Get Bike Image URL
        bike_image_url = get_bike_image_url(bike_page_soup)

        # Add Price and Color to the Dictionary
        dict_["price"] = price
        dict_["sale_price"] = sale_price
        dict_["color"] = color
        dict_["bike_image_url"] = img_url

        # Add Description 1, 2, 3 and Highlights to the Dictionary
        dict_["description_1"] = get_bike_description_1(bike_page_soup)
        dict_["description_2"] = get_bike_description_2(bike_page_soup)
        dict_["description_3"] = get_bike_description_3(bike_page_soup)
        dict_["highlights"] = get_bike_highlights(bike_page_soup)

        # Append the Dictionary to the List
        bike_details_list.append(dict_)

        end_time_ = time.time()
        print(f"Completed extraction for Bike #{index}. Time taken: {end_time_ - start_time_:.2f} seconds.")

    # Close the Driver
    finally:
        if driver:
            driver.quit()

    # Sleep for 2 seconds
    time.sleep(2)

#! End of For Loop ----

end_time = time.time()
print("\n")
print("-----------------------------------------")
print(f"Total Time Taken: {end_time - start_time:.2f} seconds.")


# Length of Bike Details List
len(bike_details_list)

# DataFrame of Bike Details
df = pd.DataFrame(bike_details_list).rename(columns = lambda x: x.replace(" ", "_").lower())
df.info()

# Drop Unnecessary Columns
df.head()


# Save DataFrame to CSV
df.to_csv("projects/cannondale/data/bikes_with_beautifulsoup_v2.csv", index=False)

