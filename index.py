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
# Request library to get dashboard HTML
import requests
# HTML scraping library
from bs4 import BeautifulSoup

load_dotenv()
usr = os.getenv("USER_NAME")
pwd = os.getenv("PASSWORD")

# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-extensions")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# URL
url = "https://caringbahhs.sentral.com.au/portal2/#!/login"

driver.get(url)

# Get timetable once in Sentral dashboard
async def scrape_timetable(url):
    data = requests.get(url)
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(data.text, "lxml")
    print(soup.find_all("div", class_="timetable table")) # tbody

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
    driver.find_element(By.CLASS_NAME, "btn btn-primary margin-bottom_20").click()