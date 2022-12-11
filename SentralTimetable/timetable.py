"""A function to get the timetable for the current week"""
# Third party imports
from selenium.webdriver import Chrome

# Local imports
from .credentials import *
from .objects import *
from .scrapers import *
from .webdriver import *

# Print the get-sentral logo
print("""
                          ╭──╮                                                \
             ╭──╮                         ╭──╮
 ╭────────╮  ╭────────╮╭──┘  ╰──╮                   ╭───────╮   ╭───────╮  ╭──\
╮╭───────╮╭──┘  ╰──╮ ╭─╮╭────╮ ╭────────╮ │  │
 │  ╭──╮  │  │  ╭──╮  │╰──╮  ╭──╯                   │  ╭────╯   │  ╭──╮ │  │  \
╰╯ ╭──╮  │╰──╮  ╭──╯ │ ╰╯╭─╮ │ ╰─────╮  │ │  │
 │  ╰──╯  │  │  ╰──╯  │   │  │                      │  ╰────╮   │  ╰──╯ │  │  \
 ╭─╯  │  │   │  │    │  ╭╯ ╰─╯ ╭─────╯  │ │  │
 ╰────╮   │  │   ╭────╯   │  │                      ╰────╮  │   │  ╭────╯  │  \
 │    │  │   │  │    │  │      │ ╭────╮ │ │  │
 ╭────╯   │  │   ╰────╮   │  ╰──╮                   ╭────╯  │   │  ╰────╮  │  \
 │    │  │   │  ╰──╮ │  │      │ ╰────╯ │ │  │
 ╰────────╯  ╰────────╯   ╰─────╯  ╭────────────╮   ╰───────╯   ╰───────╯  ╰──\
─╯    ╰──╯   ╰─────╯ ╰──╯      ╰────────╯ ╰──╯
                                   ╰────────────╯
""")
print('Created by SuperHarmony910 and J-J-B-J. Logo by cheepling.')


def __login_to_homepage(usr: str = None, pwd: str = None, url: str = None,
                        debug: bool = None, timeout: int = None) -> tuple:
    """Login to the homepage"""
    # Get credentials
    debug, usr, pwd, url, timeout = get_credentials(debug, usr, pwd, url,
                                                    timeout)

    # Create the webdriver
    if debug:
        print("Creating webdriver")
    driver = create_webdriver(headless=(not debug))

    if debug:
        print("Getting page")
    driver.get(url)

    if debug:
        print("Logging in")
    webdriver_login(driver, usr, pwd, url, timeout)

    return driver, debug, usr, pwd, url, timeout


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = None, timeout: int = None) -> Sentral:
    """Get the timetable for the current week"""

    driver, debug, usr, pwd, url, timeout = \
        __login_to_homepage(usr, pwd, url, debug, timeout)

    if debug:
        print("Scraping Timetable")
    classes = scrape_timetable(driver.page_source)
    notices = scrape_notices(driver.page_source, url)
    user = scrape_user(driver.page_source)

    if debug:
        print("Navigating to calendar")
    webdriver_go_to_calendar(driver, timeout * 2)

    if debug:
        print("Scraping Calendar")
    events = scrape_calendar(driver.page_source)

    return Sentral(
        classes=classes,
        notices=notices,
        events=events,
        user=user
    )


def set_journal(journal: str = "", usr: str = None, pwd: str = None, url: str = None,
                debug: bool = None, timeout: int = None)\
        -> None:
    """Set the journal for a given date"""

    driver, debug, usr, pwd, url, timeout = \
        __login_to_homepage(usr, pwd, url, debug, timeout)

    if debug:
        print("Saving journal")
    webdriver_save_journal(journal, driver, usr, pwd, url, timeout)
