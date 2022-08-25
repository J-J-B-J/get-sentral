"""A function to get the timetable for the current week"""
import datetime
from json import load

from scrapers import *
from webdriver import *
from credentials import *


print('Created by SuperHarmony910 and J-J-B-J')


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = None, timeout: int = 5):
    """Get the timetable for the current week"""

    # Get credentials
    credentials = get_credentials(debug, usr, pwd, url)
    debug = credentials['debug']
    usr = credentials['usr']
    pwd = credentials['pwd']
    url = credentials['url']

    # Create the webdriver
    if debug:
        print("Creating webdriver")
    driver = create_webdriver(headless=(not debug))

    if debug:
        print("Getting page")
    navigate_to_timetable(driver, usr, pwd, url, timeout)
    if debug:
        print("Logged in. Scraping Timetable")

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
