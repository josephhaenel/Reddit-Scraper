import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager  # Importing WebDriverManager

MAX_POSTS = 10  # Number of posts to scrape

BASE_URL = "https://www.reddit.com"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(subreddit_name, scrolls=3):
    """Get BeautifulSoup object for subreddit"""
    url = f"{BASE_URL}/r/{subreddit_name}" 
    driver = webdriver.Chrome()
    driver.get(url)
    for _ in range(scrolls):
        driver.implicitly_wait(10)
        driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(3, 10))
    page_content = driver.page_source
    driver.quit()

    return BeautifulSoup(page_content, 'html.parser')


def get_members(soup):
    '''Get number of members in a subreddit'''
    members_tag = soup.find("faceplate-number")
    if members_tag:
        return members_tag.get('number')
    return None

def get_post_data(soup):
    if not soup:
        return None
    
    # Extract post data
    post_data = {}
    
    # Title
    title_element = soup.find('div', {'slot': 'title'})
    post_data['title'] = title_element.text.strip() if title_element else None
    
    # Link of the Post
    link_element = soup.find('a', {'slot': 'full-post-link'})
    post_data['link'] = link_element['href'] if link_element else None
    
    # Author
    author_element = soup.find('span', class_='whitespace-nowrap')
    post_data['author'] = author_element.text.strip() if author_element else None
    
    # Avatar of the Author
    avatar_element = soup.find('faceplate-img')
    post_data['avatar'] = avatar_element['src'] if avatar_element else None
    
    # Timestamp
    timestamp_element = soup.find('faceplate-timeago')
    post_data['timestamp'] = timestamp_element['ts'] if timestamp_element else None
    
    # Comment Count
    shreddit_post = soup.find('shreddit-post')
    post_data['comment_count'] = shreddit_post['comment-count'] if shreddit_post and 'comment-count' in shreddit_post.attrs else None
    
    # Score (Thumbs Up)
    post_data['score'] = soup.get('score') if soup.get('score') else None

    return post_data

def scrape_subreddit(subreddit_name, output_file_name):
    """Scrape data for a single subreddit and write results to a .txt file."""
    soup = get_soup(subreddit_name)
    if not soup:
        return

    with open(output_file_name, 'a') as file:
        # Get members
        members = get_members(soup)
        if not members:
            print(f"r/{subreddit_name} might be private or does not exist.")
            return
        
        members_string = f"Members of r/{subreddit_name}: {members}\n"
        print(members_string)
        file.write(members_string)

        # Get data for each post
        for index, post in enumerate(soup.find_all("shreddit-post")):
            post_data = get_post_data(post)
            
            post_string = (f"Title: {post_data['title']}\n"
                        f"Score: {post_data['score']}\n"
                        f"Post Link: {post_data['link']}\n"
                        f"Thumbnail: {post_data['image_link']}\n"
                        f"Author: {post_data['author']}\n"
                        f"Creation Time: {post_data['timestamp']}\n"
                           f"{'-' * 40}\n")
            print(post_string)
            file.write(post_string)

            # Limit the number of posts for testing
            if index > MAX_POSTS:
                break

def main():
    with open("PythonScraper/subreddits.txt", "r") as f:
        subreddits = [line.strip() for line in f]

    for subreddit in subreddits:
        print(f"Scraping r/{subreddit}...")
        scrape_subreddit(subreddit, "PythonScraper/results.txt")
        print(f"Done scraping r/{subreddit}\n{'='*60}\n")

if __name__ == "__main__":
    main()
