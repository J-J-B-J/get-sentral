# Login using Selenium WebDriver
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
options = Options()
# Chrome web driver

# Environment variable libraries
# HTML scraping library
# Sleep lib

load_dotenv()
# Get credentials
usr = os.getenv("USER_NAME")
pwd = os.getenv("PASSWORD")

# Don't log unnecessary crap
options.add_argument('log-level=3')
# Invisible (headless) browser [yet to be uncommented as still in testing phase]
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager(
    chrome_type=ChromeType.CHROMIUM).install()))
# URL
url = "https://caringbahhs.sentral.com.au/portal2/#!/login"

driver.get(url)

# Get timetable once in Sentral dashboard


def scrape_timetable(html):
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    # timetable = soup(lambda tag: tag.name == 'td' and tag.get('class') == ['timetable-dayperiod'])
    # get the child 'strong' in the below asjdjkad              | down here `and tag.get('class') == ['small-caps']`
    # timetable = soup(lambda tag: tag.name in ['strong', 'small'] and tag.parent.parent.attrs.get('class') == 'timetable-class')
    # ^^ turn lambda func code to vanilla function
    timetable = soup.find_all(class_="timetable-class")
    # make a for loop that iterates a number from 0 to 3, put that through the ResultSet square brackets and get the contents of each, extract and format from there as i have no internet whilst writing this note.
    children = timetable[0].contents[0]
    print(f'descendants: {children}')

    print(timetable)
    # print(driver.find_elements(By.CLASS_NAME, "small-caps"))


# Check if you already are logged in and in the dashboard
if driver.current_url == 'https://caringbahhs.sentral.com.au/portal/dashboard':
    scrape_timetable(driver.current_url)
# If you aren't logged in, log in.
elif driver.current_url == url or driver.current_url == 'https://caringbahhs.sentral.com.au/portal2/':
    # Get
    username = driver.find_element(By.ID, 'inputEmail')
    password = driver.find_element(By.ID, 'password')
    if (username.get_attribute("value") != usr):
        username.send_keys('safin.zaman')
    password.send_keys(pwd)
    driver.find_element(By.XPATH, '//button[text()="Log In"]').click()
    time.sleep(1)
    if driver.current_url != 'https://caringbahhs.sentral.com.au/portal/dashboard':
        raise TypeError(
            "The URL is not at the specified Sentral dashboard.\n Please disable headless mode and test the code to ensure that it is functional.")
    scrape_timetable(driver.page_source)
