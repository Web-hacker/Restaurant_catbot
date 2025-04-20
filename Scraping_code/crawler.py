

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException , TimeoutException

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



time.sleep(2)  # Give page some time before first Show More


from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_show_more(driver, max_clicks=10):
    clicks_done = 0
    while clicks_done < max_clicks:
        try:
            # Wait for Show More button
            show_more = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='restaurant_list_show_more']//div[contains(text(),'Show more')]"))
            )
            try:
                show_more.click()
            except ElementClickInterceptedException:
                print("Click intercepted, trying with JS click...")
                driver.execute_script("arguments[0].click();", show_more)

            # Scroll to bottom to load new results
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Wait until new restaurants are added
            prev_count = len(driver.find_elements(By.XPATH, "//div[@data-testid='restaurant_list_card']"))
            WebDriverWait(driver, 10).until(
                lambda d: len(d.find_elements(By.XPATH, "//div[@data-testid='restaurant_list_card']")) > prev_count
            )

            clicks_done += 1
            new_count = len(driver.find_elements(By.XPATH, "//div[@data-testid='restaurant_list_card']"))
            print(f"Clicked 'Show More' ({clicks_done}/{max_clicks}) - {new_count} restaurants loaded")

        except (TimeoutException, NoSuchElementException):
            print(f"[{clicks_done + 1}/{max_clicks}] 'Show More' not clickable or missing. Ending early.")
            break



# List of cities (can add more)
city_slugs = ['kanpur']

# Setup headless Chrome
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to load all restaurants by clicking "Show More"
def load_all_restaurants(driver, max_clicks=10):
    for i in range(max_clicks):
        try:
            time.sleep(2)  # let new content settle
            show_more = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Show More')]"))
            )
            
            # Scroll into view and wait
            driver.execute_script("arguments[0].scrollIntoView(true);", show_more)
            time.sleep(1)

            # Try to click via JS (avoids interception)
            driver.execute_script("arguments[0].click();", show_more)
            print(f"Clicked 'Show More' ({i+1}/{max_clicks})")
            time.sleep(3)  # wait for more content to load

        except Exception as e:
            print(f"[{i+1}/{max_clicks}] 'Show More' not clickable or missing: {e}")
            break


def scrape_restaurants(driver,city):
    time.sleep(2)  # Give time after final 'Show More' click
    restaurant_elements = driver.find_elements(By.XPATH, "//div[@data-testid='restaurant_list_card']")

    restaurants = []
    for res in restaurant_elements:
        try:
            name = res.find_element(By.XPATH, ".//div[contains(@class,'eLaouz')]").text
            cuisine = res.find_element(By.XPATH, ".//div[contains(@class,'bfOHNR')]").text
            link = res.find_element(By.CLASS_NAME,'kcEtBq').get_attribute("href")
            rating = res.find_element(By.XPATH, ".//div[contains(@class,'hhnNfO')]").text

            restaurants.append({
                "name": name,
                "cuisine": cuisine,
                "rating": rating,
                "link":link,
                "city":city,
                #"delivery_time": delivery_time
            })
        except Exception as e:
            print("Error parsing restaurant:", e)
    return restaurants


# Function to extract data from page source using BeautifulSoup
def extract_data(city, html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('a', class_='kcEtBq')
    restaurants = []

    for card in cards:
        try:
            name = card.find('div', class_='eLaouz').text
            cuisines = card.find('div',class_ = 'bfOHNR').text
            rating = card.find('div', class_='hhnNfO').text if card.find('div', class_='hhnNfO') else "N/A"
            #time_text = card.find_all('div')[3].text

            restaurants.append({
                'City': city,
                'Name': name,
                'Cuisines': cuisines,
                'Rating': rating,
                #'Delivery Time': time_text
            })
        except Exception as e:
            print("Parse error:", e)

    return restaurants

# Main function
def scrape_multiple_cities_to_csv(city_slugs, output_file="swiggy_restaurants_kanpur.csv"):
    all_data = []
    for city in city_slugs:
        print(f"\nScraping city: {city}...")
        url = f"https://www.swiggy.com/city/{city}/order-online"

        driver = get_driver()
        driver.get(url)
        time.sleep(3)

        #load_all_restaurants(driver, max_clicks=10)
        click_show_more(driver,max_clicks=10)
        html = driver.page_source
        #print(html)
        #city_data = extract_data(city, html)
        city_data = scrape_restaurants(driver,city)
        all_data.extend(city_data)

        driver.quit()
        print(f"✔ Scraped {len(city_data)} restaurants from {city}.")

    # Save to single CSV
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"\n✅ All data saved to: {output_file}")

# Run the scraper
if __name__ == "__main__":
    scrape_multiple_cities_to_csv(city_slugs)


