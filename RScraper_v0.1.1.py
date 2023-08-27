import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json

'''Constants'''
MAX_POSTS = 10  # Maximum number of posts to be scraped
BASE_URL = 'https://www.reddit.com/r/'  # Base URL of a subreddit


def getSoupObj(subreddit, scrolls=3):
    '''Returns a BeautifulSoup object for a given subreddit'''
    driver_path = os.path.join(os.path.dirname(
        __file__), 'resources', 'chromedriver.exe')
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(BASE_URL + subreddit)
    time.sleep(2)
    for _ in range(scrolls):
        driver.implicitly_wait(10)
        driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup


def getTotalMembers(subredditSoupObj):
    '''Returns the total number of members in a given subreddit'''
    membersIdentifier = subredditSoupObj.find("faceplate-number")
    if not membersIdentifier:
        raise Exception(f"Members identifier of {subredditSoupObj} not found")
    # Extracts number and removes commas
    return int(membersIdentifier['number'])


def getTitle(subredditSoupObj):
    '''Returns the title of a subreddit post'''
    postTitle = subredditSoupObj.find("div", {"slot": "title"})
    if not postTitle:
        raise Exception(f"Post title for {subredditSoupObj} not found")
    return postTitle.text.strip()


def getAuthor(subredditSoupObj):
    '''Returns the author of a subreddit post'''
    author = subredditSoupObj.find("span", class_="whitespace-nowrap")
    if not author:
        raise Exception(f"Author for {subredditSoupObj} not found")
    return author.text.strip()


def getTimeStamp(subredditSoupObj):
    '''Returns the time stamp for a subreddit post'''
    postTimeStamp = subredditSoupObj.find("faceplate-timeago")
    if not postTimeStamp:
        raise Exception(f"Post time stamp for {subredditSoupObj} not found")
    timeTag = postTimeStamp.find('time')
    if not timeTag:
        raise Exception(f"Post time tag for {postTimeStamp} not found")
    return timeTag['datetime']


def getThumbsUp(subredditSoupObj):
    '''Returns the number of "likes" for a subreddit post'''
    thumbsUp = subredditSoupObj.get("score")  # Not sure if this works right
    if not thumbsUp:
        return 0  # Post probably doesn't have any "likes"
    return thumbsUp


''' TODO: Could add link to post, authorAvatar, link to image, etc'''


def scrape_subreddit(subreddit, output_file=os.path.join(os.path.dirname(__file__), 'IO', 'output.json')):
    '''Scrape data from a subreddit and write it to output.json'''
    subredditSoupObj = getSoupObj(subreddit)
    if not subredditSoupObj:
        raise Exception(f"Could not get subreddit object for {subreddit}")

    results = []

    totalMembers = getTotalMembers(subredditSoupObj)
    totalMembersString = f"Members of r/{subreddit}: {totalMembers}\n"
    print(totalMembersString)

    results.append({"Subreddit": subreddit, "Members": totalMembers})

    for index, post in enumerate(subredditSoupObj.find_all("shreddit-post")):
        postData = {
            "Title": getTitle(post),
            "Author": getAuthor(post),
            "TimeStamp": getTimeStamp(post),
            "ThumbsUp": getThumbsUp(post)
        }
        results.append(postData)

        if index > MAX_POSTS:
            break

    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)


def main():
    '''Main function'''
    # Opening the "subreddits.txt" file which contains the subreddits to be scraped
    with open(os.path.join(os.path.dirname(__file__), 'IO', 'subreddits.txt'), 'r') as f:
        subreddits = [line.strip() for line in f]

    # Iterating through the subreddits and calling the scrape_subreddit function for each one
    for subreddit in subreddits:
        print(f"Scraping {subreddit}...")
        scrape_subreddit(subreddit)
        print(f"Finished scraping {subreddit}\n{'='*60}\n")


if __name__ == '__main__':
    main()
