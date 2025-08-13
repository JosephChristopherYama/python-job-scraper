
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jobs(url):
  
    try:
        
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        
        soup = BeautifulSoup(response.text, 'html.parser')

        
        job_cards = soup.find_all('div', class_='job-card')

        if not job_cards:
            print("No job cards found. The website structure might have changed.")
            return []

        job_data = []
        
        for card in job_cards:
            title_element = card.find('h2', class_='job-title')
            company_element = card.find('p', class_='company-name')
            location_element = card.find('span', class_='location')

            
            title = title_element.text.strip() if title_element else 'N/A'
            company = company_element.text.strip() if company_element else 'N/A'
            location = location_element.text.strip() if location_element else 'N/A'

            job_data.append({
                'Title': title,
                'Company': company,
                'Location': location
            })
            
        return job_data

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_to_csv(data, filename='job_postings.csv'):
   
    if not data:
        print("No data to save.")
        return

    
    df = pd.DataFrame(data)

    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}")



if __name__ == "__main__":
   
    TARGET_URL = 'https://realpython.github.io/fake-jobs/' # Using a safe, legal-to-scrape example site

    print(f"Scraping job postings from: {TARGET_URL}")
    
   
    scraped_data = scrape_jobs(TARGET_URL)

   
    if scraped_data:
        save_to_csv(scraped_data)
