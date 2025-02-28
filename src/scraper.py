import os
import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

# Constants
BASE_URL = "https://ffnews.com/category/newsarticle/"
MAX_RETRIES = 3
RETRY_DELAY = 5
PAGE_LOAD_TIMEOUT = 60
REQUEST_DELAY = 2

def convert_date(raw_date):
    """Convert timestamp to YYYY-MM-DD format"""
    try:
        date_obj = datetime.strptime(raw_date, "%B %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown Date"

def fetch_and_parse(driver):
    """Fetch the content of the current page and parse it with BeautifulSoup."""
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ff__single__feed__post"))
    )
    time.sleep(2)  
    return BeautifulSoup(driver.page_source, "html.parser")

def get_article_details(driver, article_url):
    """Extracts title and date from an article page using Selenium and BeautifulSoup."""
    driver.get(article_url)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        title_tag = soup.find("h1")
        date_tag = soup.find("p", class_="post__date")
        title = title_tag.text.strip() if title_tag else "No title"
        raw_date = date_tag.text.strip() if date_tag else "No date"
        date = convert_date(raw_date)
        return title, date
    except Exception as e:
        print(f"Error extracting article details {article_url}: {e}")
        return "No title", "No date"

def scrape_ffnews(output_file="../data/ffnews_data.csv"):
    """Scrapes article links using Selenium and extracts details with BeautifulSoup."""
    options = Options()
    options.headless = True  
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    
    file_exists = os.path.exists(output_file)
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Headline", "Timestamp"])
        
        visited_articles = set()
        while True:
            soup = fetch_and_parse(driver)
            articles = soup.find_all("div", class_="col-sm-6 col-lg-4 ff__single__feed__post mb-3")
            if not articles:
                print("No more articles found. Stopping.")
                break
            
            for article in articles:
                try:
                    link_tag = article.find("div", class_="d-block justify-content-between align-items-top single__info__data").find("a", href=True)
                    if link_tag:
                        article_url = link_tag["href"]
                        if article_url in visited_articles:
                            continue 
                        
                        title, date = get_article_details(driver, article_url)
                        writer.writerow([title, date])
                        visited_articles.add(article_url)
                        print(f"Scraped: {title} ({date})")
                        driver.get(BASE_URL)  
                        time.sleep(2)
                except Exception as e:
                    print(f"Error processing article: {e}, moving to next.")
                    continue
            
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "next page-numbers"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(2)
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)  
            except Exception as e:
                print("No more pages to load. Stopping.")
                break
    
    driver.quit()

if __name__ == "__main__":
    scrape_ffnews()
