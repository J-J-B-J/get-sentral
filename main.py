"""A function to get the timetable for the current week"""
# Created by SuperHarmony910 !

# Login using Selenium WebDriver
import time
from bs4 import BeautifulSoup
import os
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from json import load


def scrape_timetable(html):
    """Scrape the HTML for the timetable"""
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    timetable = soup.find_all(class_="timetable-class")
    classes = []
    for i in range(4):
        try:
            class_name = timetable[i].contents[1].contents[1].string
        except IndexError:
            class_name = "Unknown"
        try:
            class_room = timetable[i].small.find_all("strong")[0].string
        except IndexError:
            class_room = "Unknown"
        try:
            class_teacher = timetable[i].small.find_all("strong")[1].string
        except IndexError:
            class_teacher = "Unknown"
        class_ = {
            "subject": class_name,
            "room": class_room,
            "teacher": class_teacher
        }
        classes.append(class_)
    return classes


def get_data_from_json(json_file):
    """Get the data from the json file"""
    try:
        with open(json_file, 'r') as f:
            return load(f)
    except:
        return None


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = False):
    """Get the timetable for the current week"""
    # Chrome web driver
    if debug:
        print("Getting chrome driver options")
    options = Options()

    # Get credentials
    if debug:
        print("Getting Credentials")
    if not usr:
        usr = os.getenv("USER_NAME")
        if not usr:
            usr = get_data_from_json("Sentral_Details.json")["USERNAME"]
            if not usr:
                usr = input("Username: ")
    if not pwd:
        pwd = os.getenv("PASSWORD")
        if not pwd:
            pwd = get_data_from_json("Sentral_Details.json")["PASSWORD"]
            if not pwd:
                pwd = input("Password: ")
    if not url:
        url = os.getenv("URL")
        if not url:
            url = get_data_from_json("Sentral_Details.json")["URL"]
            if not url:
                url = input("URL: ")

    # Create the webdriver
    if debug:
        print("Creating webdriver")

    # Don't log unnecessary stuff
    options.add_argument('log-level=3')
    # Invisible (headless) browser
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options,
                              service=Service(ChromeDriverManager().install()))

    # Get the page
    if debug:
        print("Getting page")
    driver.get(url)

    # Get timetable once in Sentral dashboard

    # Check if you already are logged in and in the dashboard
    if driver.current_url.endswith('/portal/dashboard'):
        if debug:
            print("Already logged in - Scraping Timetable")
        return scrape_timetable(driver.current_url)
    # If you aren't logged in, log in.
    elif driver.current_url == url or driver.current_url.endswith('/portal2/'):
        if debug:
            print("Not logged in - Logging in")
        # Get
        username = driver.find_element(By.ID, 'inputEmail')
        password = driver.find_element(By.ID, 'password')
        if username.get_attribute("value") != usr:
            username.send_keys(usr)
        password.send_keys(pwd)
        driver.find_element(By.XPATH, '//button[text()="Log In"]').click()
        time.sleep(2.5)
        if not driver.current_url.endswith('/portal/dashboard'):
            raise TypeError(
                "The URL is not at the specified Sentral dashboard.\n Please "
                "disable headless mode and test the code to ensure that it is "
                "functional.")
        if debug:
            print("Logged in - Scraping Timetable")
        return scrape_timetable(driver.page_source)


if __name__ == "__main__":
    print(get_timetable())
