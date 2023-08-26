# Reddit Scraper using Python

This is a simple scraper to extract data from given Reddit subreddits.

## Installation

First, clone the repository: `git clone github.com/josephhaenel/PythonScraper`

Navigate to the directory: 
`cd PythonScraper`

You might want to set up a virtual environment (optional but recommended):

`python3 -m venv venv`
`source venv/bin/activate`  # On Windows, use `venv\Scripts\activate`

Install the required dependencies:

`pip install requests selenium beautifulsoup4 webdriver_manager`

## Usage

Add the list of subreddits you want to scrape in PythonScraper/subreddits.txt (one subreddit per line), then run:

`python RedditScraper.py` # or the name you've given this script

### Dependencies

    requests
    selenium
    beautifulsoup4
    webdriver_manager

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


#### Remember that web scraping can be against the terms of service of some websites. Ensure that you're following Reddit's terms and conditions when you're scraping, and always respect `robots.txt`.
