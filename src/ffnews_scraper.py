from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv 

def convert_date(raw_date):
    """convert timestamp to YYYY-MM-DD format"""
    try:
        date_obj = datetime.strptime(raw_date, "%B %d %Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return "Unknown Date"
    
def scrape_ffnews(query="finance", output_file="../data/ffnews_data.csv"):
    page = 1
    base_url = f"https://ffnews.com/?s={query}#"
    
    # append data in file once it's captured
    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Headline", "Timestamp"])
        
        while True:
            url = base_url + str(page)
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to fetch page {page}. Stopping.")
                break
            
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("div", class_="col-sm-6 col-lg-4 ff__single__feed__post mb-3")
            
            if not articles:
                print("No more articles found. Stopping.")
                break
            
            for article in articles:
                title_tag = article.find("h3")
                date_tag = article.find("date")
                
                title = title_tag.text.strip() if title_tag else "No title"
                raw_timestamp = date_tag.text.strip() if date_tag else "No date"
                date = convert_date(raw_timestamp)

                writer.writerow([title, date])
            
            page += 1


if __name__ == "__main__":
    scrape_ffnews()
