
import time
import pandas as pd
import csv
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
city_slugs = ['kanpur','mumbai','delhi','pune','banglore']

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


import re

def scrape_restaurants(driver):
    time.sleep(2)
    restaurant_name = driver.find_element(By.XPATH,"//h1").text
    print(restaurant_name)
    restaurant_location = driver.find_element(By.XPATH,"//div[contains(@class,'_2gTwA')]").text
    print(restaurant_location)

    titles = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'cid-')]")
    dishes = []

    for title in titles:
        # Get all headers (section names like 'Veg Pizza (6)', etc.)
        headers = title.find_elements(By.XPATH, ".//h3")
        
        # Build a list of tuples: (cleaned_tag, count)
        tag_count_list = []
        for h in headers:
            text = h.text
            match = re.search(r'\((\d+)\)', text)
            count = int(match.group(1)) if match else 1
            clean_tag = re.sub(r'\s*\(\d+\)', '', text).strip()
            tag_count_list.append((clean_tag, count))

        # Fetch all dish items under this block
        dish_items = title.find_elements(By.XPATH, ".//div[@data-testid='normal-dish-item']")

        idx = 0
        for tag, count in tag_count_list:
            print(tag)
            for _ in range(count):
                if idx >= len(dish_items):
                    break  # Avoid IndexError if less items than stated
                dish = dish_items[idx]
                idx += 1
                try:
                    name = dish.find_element(By.XPATH, ".//div[contains(@class,'dwSeRx')]").text
                except:
                    name = 'N/A'
                try:
                    info = dish.find_element(By.XPATH, ".//p[contains(@class,'_1QbUq')]").text
                except:
                    info = 'N/A'
                try:
                    rating = dish.find_element(By.XPATH, ".//div[contains(@class,'sc-gEvEer')]").text
                except:
                    rating = 'N/A'
                complete_info = dish.text

                dishes.append({
                    "cuisine_name": name,
                    "Complete Info": complete_info,
                    "Restaurant_Location": restaurant_location,
                    "dish_tags": tag
                })

    return dishes, restaurant_name


# Main function
def scrape_multiple_cities_to_csv(output_file="complete_kanpur_restaurants_dishes.csv"):
    all_data = []
    restaurant_links = []
    with open("swiggy_restaurants_kanpur.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            restaurant_links.append(row['link']) 
    for link in restaurant_links:
        print(f"\nScraping from: {link}...")
        url = f"{link}"

        driver = get_driver()
        driver.get(url)
        time.sleep(3)

        dishes_data,restaurant_name = scrape_restaurants(driver)
        all_data.extend(dishes_data)

        driver.quit()
        print(f"✔ Scraped {len(dishes_data)} dishes from {link}.")
        df = pd.DataFrame(dishes_data)
        output = f"{restaurant_name}_dishes.csv"
        df.to_csv(output, index=False)
        print(f"\n✅ All data saved to: {output}")

    # Save to single CSV

    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"\n✅ All data saved to: {output_file}")

# Run the scraper
if __name__ == "__main__":
    scrape_multiple_cities_to_csv()




