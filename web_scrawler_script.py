import asyncio
import aiohttp
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading

# Semaphore for controlling concurrency
SEM_LIMIT = 5  

# Function to set up Selenium
def setup_selenium():
    options = Options()
    options.headless = True  # Run in headless mode (without a browser window)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver



# Function to scrape Amazon product URLs
def get_amazon_products(category, output_file):
    search_url = f"https://www.amazon.in/s?k={category.replace(' ', '+')}"
    driver = setup_selenium()
    
    product_urls = set()
    page_number = 1  # Track the current page number

    with open(output_file, 'a') as file:  # Open the file for appending URLs
        while True:
            print(f"Scraping Amazon {category} page {page_number}...")

            driver.get(search_url)
            time.sleep(3)  # Wait for the page to load

            # Extract all product URLs on the current page
            links = driver.find_elements(By.CSS_SELECTOR, 'a[href]')
            for link in links:
                href = link.get_attribute('href')
                if re.search(r'/dp/|/gp/', href):
                    product_url = href.split('?')[0]  # Remove query params
                    product_urls.add(product_url)

            print(f"Found {len(product_urls)} product URLs so far")

            # Write product URLs to file
            for url in product_urls:
                file.write(f"{url}\n")  # Write each URL on a new line

            # Try to find the next page using 's-pagination-item'
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, 'a.s-pagination-item.s-pagination-next')
                next_page.click()  # Click the "Next" button to go to the next page
                time.sleep(3)  # Add a delay to simulate user behavior and avoid bot detection
                page_number += 1  # Increment page number
            except:
                print("No more pages or unable to find the Next button.")
                break

    driver.quit()
    return len(product_urls)

# Asynchronous wrapper for the Amazon scraper
async def scrape_amazon(session, category, output_file):
    # Run the blocking function in a separate thread
    loop = asyncio.get_event_loop()
    total_urls = await loop.run_in_executor(None, get_amazon_products, category, output_file)
    print(f"Total product URLs for {category}: {total_urls}")

async def scrape_flipkart(session, category, output_file):
    # Can Implement scraping logic for Flipkart, including pagination
    pass

async def scrape_myntra(session, category, output_file):
    #  Can Implement scraping logic for Myntra, including infinite scroll handling
    pass

async def scrape_domain(session, domain, category, output_file):
    async with SEMAPHORE:  # Limit the number of concurrent requests

        # Todo: Use hasp map or database instead of multiple if else
        if domain == 'amazon':
            await scrape_amazon(session, category, output_file)
        elif domain == 'flipkart':
            await scrape_flipkart(session, category, output_file)
        elif domain == 'myntra':
            await scrape_myntra(session, category, output_file)

# Async function to handle scraping for all domains
async def scrape_all(domains, output_file):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for domain, categories in domains.items():
            for category in categories:
                tasks.append(scrape_domain(session, domain, category, output_file))
        
        await asyncio.gather(*tasks)

# Main function to initiate scraping
def main():
    # Input: domains and categories
    domains = {
        "amazon": ["Laptops", "Mobiles"],
        "flipkart": ["TVs", "Washing Machines"],
        "myntra": ["nightdress"],
        # Add more domains and categories as needed
    }
    
    # Output file for storing product URLs
    output_file = "product_urls.json"

    # Create a semaphore for controlling concurrency
    global SEMAPHORE
    SEMAPHORE = asyncio.Semaphore(SEM_LIMIT)

    # Run asyncio event loop
    asyncio.run(scrape_all(domains, output_file))

if __name__ == "__main__":
    main()
