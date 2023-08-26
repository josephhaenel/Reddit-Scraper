import time
import random
import requests
import zipfile
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager  # Possiblly deprecated

'''Constants'''
MAX_POSTS = 10  # Maximum number of posts to be scraped
BASE_URL = 'https://www.reddit.com/r/'  # Base URL of a subreddit
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def getSoupObj(subreddit, scrolls=3):
    '''Returns a BeautifulSoup object for a given subreddit'''
    driver_path = os.path.join(os.path.dirname(
        __file__), 'resources', 'chromedriver.exe')
    driver = webdriver.Chrome(executable_path= driver_path)
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
    return postTitle


def getAuthor(subredditSoupObj):
    '''Returns the author of a subreddit post'''
    author = subredditSoupObj.find("span", class_="whitespace-nowrap")
    if not author:
        raise Exception(f"Author for {subredditSoupObj} not found")
    return author


def getTimeStamp(subredditSoupObj):
    '''Returns the time stamp for a subreddit post'''
    postTimeStamp = subredditSoupObj.find("faceplate-timeago")
    if not postTimeStamp:
        raise Exception(f"Post time stamp for {subredditSoupObj} not found")
    return postTimeStamp


# def getCommentCount(subredditSoupObj):
#     '''Returns the number of comments for a subreddit post'''
#     commentCount = subredditSoupObj.find(
#         "commentcount")  # Not sure if this works right
#     if not commentCount:
#         raise Exception(f"Comment Count for {subredditSoupObj} not found")
#     return commentCount


def getThumbsUp(subredditSoupObj):
    '''Returns the number of "likes" for a subreddit post'''
    thumbsUp = subredditSoupObj.get("score")  # Not sure if this works right
    if not thumbsUp:
        raise Exception(f"Thumbs up for {subredditSoupObj} not found")
    return thumbsUp


''' Could add link to post, authorAvatar, link to image, etc'''


def scrape_subreddit(subreddit, output_file=os.path.join(os.path.dirname(__file__), 'IO', 'output.txt')):
    '''Scrape data from a subreddit and write it to output.txt'''
    subredditSoupObj = getSoupObj(subreddit)
    if not subredditSoupObj:
        raise Exception(f"Could not get subreddit object for {subreddit}")

    with open(output_file, 'a') as file:
        # Calling getTotalMembers function to get total members
        totalMembers = getTotalMembers(subredditSoupObj)
        # String for total members to print and output to file
        totalMembersString = f"Members of r/{subreddit}: {totalMembers}\n"
        # Print the total members out to terminal for user interaction
        print(totalMembersString)
        file.write(totalMembersString)  # Writing total members to output_file

        # Secret Sauce
        for index, post in enumerate(subredditSoupObj.find_all("shreddit-post")):
            postData = {
                "Title": getTitle(post),
                "Author": getAuthor(post),
                "TimeStamp": getTimeStamp(post),
                # "CommentCount": getCommentCount(post),
                "ThumbsUp": getThumbsUp(post)
            }

            # String to be printed out and output to file
            outputString = (
                f"Title:            {postData['Title']}         \n"
                f"Author:           {postData['Author']}        \n"
                f"TimeStamp:        {postData['TimeStamp']}     \n"
                # f"CommentCount:     {postData['CommentCount']}  \n"
                f"ThumbsUp:         {postData['ThumbsUp']}      \n"
                f"{'-' * 40}\n"
            )

            print(outputString)
            file.write(outputString)

            # TODO: Remove Later... Limits number of posts for testing
            if index > MAX_POSTS:
                break


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
