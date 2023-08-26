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

`python RScraper_v#.#.#.py` # or the name you've given this script

### Dependencies

selenium: for automating browser actions.
BeautifulSoup4: for parsing HTML and extracting required information.

You can install them using `pip install selenium beautifulsoup4`

### Chromedriver setup *REQUIRED*

The script uses Chromedriver to interact with the Chrome browser. To get it running, follow these steps:
    1. Download the appropriate version of Chromedriver for your system from https://googlechromelabs.github.io/chrome-for-testing/
    2. Extract the downloaded file
    3. Place the *chromedriver.exe* in the *resources* directory of the project

Ensure that the version of Chromedriver you download is compatible with the version of Chrome installed on your system

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


#### Remember that web scraping can be against the terms of service of some websites. Ensure that you're following Reddit's terms and conditions when you're scraping, and always respect `robots.txt`.
