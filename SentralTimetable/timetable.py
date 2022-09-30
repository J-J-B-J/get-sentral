"""A function to get the timetable for the current week"""

try:
    from . import credentials as creds
    from . import scrapers
    from . import webdriver
except ImportError:
    import credentials as creds
    import scrapers
    import webdriver

with open('SentralTimetable/get_sentral.txt', 'r') as f:
    print(f.read())
print('Created by SuperHarmony910 and J-J-B-J')


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = None, timeout: int = None) -> dict:
    """Get the timetable for the current week"""
    data = {}

    # Get credentials
    debug, usr, pwd, url, timeout = creds.get(debug, usr, pwd, url, timeout)

    # Create the webdriver
    if debug:
        print("Creating webdriver")
    driver = webdriver.create(headless=(not debug))

    if debug:
        print("Getting page")
    driver.get(url)

    if debug:
        print("Logging in")
    webdriver.login(driver, usr, pwd, url, timeout)

    if debug:
        print("Scraping Timetable")
    data['classes'] = scrapers.scrape_timetable(driver.page_source)
    data['notices'] = scrapers.scrape_notices(driver.page_source)

    if debug:
        print("Navigating to calendar")
    webdriver.go_to_calendar(driver, timeout * 2)

    if debug:
        print("Scraping Calendar")
    data['events'] = scrapers.scrape_calendar(driver.page_source)

    return data
