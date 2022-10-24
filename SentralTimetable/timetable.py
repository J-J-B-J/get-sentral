"""A function to get the timetable for the current week"""

from .credentials import *
from .scrapers import *
from .webdriver import *
from .objects import *

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
print('Created by SuperHarmony910 and J-J-B-J')


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = None, timeout: int = None) -> Sentral:
    """Get the timetable for the current week"""

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

    if debug:
        print("Scraping Timetable")
    classes = scrape_timetable(driver.page_source)
    notices = scrape_notices(driver.page_source)
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
