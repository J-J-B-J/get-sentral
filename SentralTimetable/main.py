"""A function to get the timetable for the current week"""
# Login using Selenium WebDriver
import datetime
import time
from bs4 import BeautifulSoup
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from json import load


print('Created by SuperHarmony910 and J-J-B-J')


def scrape_timetable(html: str):
    """Scrape the HTML for the timetable"""
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    data = {'classes': {}, 'notices': []}
    try:
        timetable_periods = soup.find(class_="timetable table").find_all('tr')
    except AttributeError:
        return data
    for period in timetable_periods:
        if 'inactive' in period.find('td')['class']:
            class_ = None
        else:
            try:
                class_name = period.find_all('strong')[0].string
            except IndexError:
                class_name = "Unknown"
            try:
                class_room = period.find_all('strong')[1].string
            except IndexError:
                class_room = "Unknown"
            try:
                class_teacher = period.find_all("strong")[2].string
            except IndexError:
                class_teacher = "Unknown"
            class_ = {
                "subject": class_name,
                "room": class_room,
                "teacher": class_teacher
            }
        class_number = period.find('th').string
        data['classes'][class_number] = class_

    notices = soup.find_all(class_='notice-wrap')
    for notice in notices:
        notice_title = notice.find('h4').string
        notice_teacher = notice.find_all('strong')[1].string.strip()
        notice_date = \
            str(notice.find('small').contents[2]).strip().lstrip('on ').split()
        try:
            day = int(notice_date[1])
        except ValueError:
            day = 0
        try:
            month = ['', 'January', 'February', 'March', 'April', 'May',
                     'June', 'July', 'August', 'September', 'October',
                     'November', 'December'].index(notice_date[2].rstrip(','))
        except ValueError:
            month = 0
        try:
            year = int(notice_date[3])
        except ValueError:
            year = 0
        try:
            hour = int(notice_date[5].split(':')[0])
        except ValueError:
            hour = 0
        try:
            minute = int(notice_date[5].split(':')[1][:-2])
        except ValueError:
            minute = 0
        if notice_date[5].split(':')[1][-2:] == 'pm':
            hour += 12
        notice_date = (year, month, day, hour, minute)
        notice_content = ""
        for tag in notice.find_all('p'):
            notice_content += ' '.join(tag.strings) + '\n'

        notice_data = {
            'title': notice_title,
            'teacher': notice_teacher,
            'date': notice_date,
            'content': notice_content
        }
        data['notices'].append(notice_data)
    return data


def get_data_from_json(json_file):
    """Get the data from the json file"""
    try:
        with open(json_file, 'r') as f:
            return load(f)
    except:
        return {}


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = None, timeout: int = 5):
    """Get the timetable for the current week"""
    # Chrome web driver
    if debug:
        print("Getting chrome driver options")
    options = Options()

    # Get credentials
    # Use "is None" instead of "not" for debug because debug could be False
    if debug is None:
        debug = {"True": True, "False": False}.get(os.getenv("DEBUG"))
        if debug is None:
            debug = get_data_from_json("Sentral_Details.json").get("DEBUG")
            if debug is None:
                while True:
                    debug = {"Y": True, "N": False}.get(input("Debug? Y/N: "))
                    if debug is not None:
                        break
    if not usr:
        usr = os.getenv("USER_NAME")
        if not usr:
            usr = get_data_from_json("Sentral_Details.json").get("USERNAME")
            if not usr:
                usr = input("Username: ")
    if not pwd:
        pwd = os.getenv("PASSWORD")
        if not pwd:
            pwd = get_data_from_json("Sentral_Details.json").get("PASSWORD")
            if not pwd:
                pwd = input("Password: ")
    if not url:
        url = os.getenv("URL")
        if not url:
            url = get_data_from_json("Sentral_Details.json").get("URL")
            if not url:
                url = input("URL: ")

    # Create the webdriver
    if debug:
        print("Creating webdriver")

    # Don't log unnecessary stuff
    options.add_argument('log-level=3')
    # Invisible (headless) browser
    if not debug:
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
    if debug:
        print(f"Driver URL: {driver.current_url}")
    if driver.current_url.endswith('/portal/dashboard'):
        if debug:
            print("Already logged in - Scraping Timetable")
        return scrape_timetable(driver.current_url)
    # If you aren't logged in, log in.
    elif driver.current_url == url or '/portal2/' in driver.current_url:
        if debug:
            print("Not logged in - Logging in")
        # Get
        username = driver.find_element(value='inputEmail')
        password = driver.find_element(value='password')
        if username.get_attribute("value") != usr:
            username.send_keys(usr)
        password.send_keys(pwd)
        driver.find_element(By.XPATH, '//button[text()="Log In"]').click()
        start_time = time.time()
        while True:
            if driver.current_url.endswith('/portal/dashboard'):
                break
            elif time.time() > start_time + timeout:
                raise TypeError(
                    "The URL is not at the specified Sentral dashboard.\n "
                    "Please disable headless mode and test the code to ensure "
                    "that it is functional. The page may also have failed to "
                    "load in 5 secs. You can change the timeout by passing a "
                    "value to the timeout arguement"
                )
        if debug:
            print("Logged in - Scraping Timetable")
        return scrape_timetable(driver.page_source)


if __name__ == "__main__":
    timetable = get_timetable()

    print("\n\nCLASSES\n")
    for my_period, my_class in timetable['classes'].items():
        if my_class:
            print(
                f"{my_period}: {my_class['subject']} in {my_class['room']}"
                f" with {my_class['teacher']}"
            )
        else:
            print(f"{my_period}: Empty")

    print("\n\nNOTICES\n")
    for my_notice in timetable['notices']:
        print(my_notice['title'].upper())
        print('-' * len(my_notice['title']))
        d = my_notice['date']
        my_notice_date = datetime.datetime(d[0], d[1], d[2], d[3], d[4])\
            .strftime('%a, %d %b at %I:%M%p')
        print(f"By {my_notice['teacher']} on {my_notice_date}")
        print('-' * len(my_notice['title']))
        print(my_notice['content'] + '\n')
