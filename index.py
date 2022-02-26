# Login using Selenium WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
options = Options()
# Chrome web driver
from webdriver_manager.chrome import ChromeDriverManager

# Environment variable libraries
import os
from dotenv import load_dotenv
# HTML scraping library
from bs4 import BeautifulSoup
# Sleep lib
import time

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

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# URL
url = "https://caringbahhs.sentral.com.au/portal2/#!/login"

driver.get(url)

# Get timetable once in Sentral dashboard
def scrape_timetable(html):
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    timetable = soup(lambda tag: tag.name == 'td' and tag.get('class') == ['timetable-dayperiod'])
    print(timetable)

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
    time.sleep(5)
    if driver.current_url == 'https://caringbahhs.sentral.com.au/portal/dashboard':
        scrape_timetable(driver.page_source)
    else:
        print('The program failed...')
    