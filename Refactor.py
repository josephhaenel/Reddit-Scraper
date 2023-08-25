import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager # Possiblly deprecated

'''Constants'''
MAX_POSTS = 10 # Maximum number of posts to be scraped
BASE_URL = 'https://www.reddit.com/r/' # Base URL of a subreddit
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def getSoupObj(subreddit, scrolls = 3):
    '''Returns a BeautifulSoup object for a given subreddit'''
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(BASE_URL + subreddit)
    time.sleep(2)
    for _ in range(scrolls):
        driver.implicitly_wait(10)
        driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def scrape_subreddit(subreddit, output_file= os.path.join(os.path.dirname(__file__)) + 'I/O_Files/output.txt'):
    '''Scrape data from a subreddit and write it to output.txt'''
    subredditSoupObj = getSoupObj(subreddit)
    if not subredditSoupObj:
        raise Exception(f"Could not get subreddit object for {subreddit}")
    
    

'''Main function'''

def main():
    # Opening the "subreddits.txt" file which contains the subreddits to be scraped
    with open(os.path.join(os.path.dirname(__file__) + "subreddits.txt"), 'r') as f:
        subreddits = [line.strip() for line in f]
    
    # Iterating through the subreddits and calling the scrape_subreddit function for each one
    for subreddit in subreddits:
        print(f"Scraping {subreddit}...")
        scrape_subreddit(subreddit)
        print(f"Finished scraping {subreddit}\n{'='*60}\n")

if __name__ == '__main__':
    main()