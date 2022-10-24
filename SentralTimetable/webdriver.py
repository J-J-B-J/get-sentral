"""Functions to simplify use of the webdriver"""
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def create_webdriver(headless: bool) -> webdriver.Chrome:
    """
    Create a webdriver object
    :param headless: Weather or not to make the webdriver headless
    :return: The webdriver object
    """
    options = Options()
    # Don't log unnecessary stuff
    options.add_argument('log-level=0')
    # Invisible (headless) browser
    if headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

    return webdriver.Chrome(options=options,
                            service=Service(ChromeDriverManager().install()))


def webdriver_login(driver: webdriver.Chrome, usr: str, pwd: str, url: str,
                    timeout: int = 5) -> None:
    """
    Login to the Sentral dashboard
    :param driver: The webdriver object to use
    :param usr: The username to use
    :param pwd: The password to use
    :param url: The URL to use
    :param timeout: The time to wait for the page to load
    :return: None
    """
    # If you aren't logged in, log in.
    if (not driver.current_url.endswith('/portal/dashboard')) and \
            driver.current_url == url or '/portal2/' in driver.current_url:
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
                return
            elif time.time() > start_time + timeout:
                raise TypeError(
                    "The URL is not at the specified Sentral dashboard.\n "
                    "Please disable headless mode and test the code to ensure "
                    "that it is functional. The page may also have failed to "
                    "load in 5 secs. You can change the timeout by passing a "
                    "value to the timeout arguement"
                )


def webdriver_go_to_calendar(driver: webdriver.Chrome, timeout: int = 5) -> \
        None:
    """
    Navigate to the calendar page from the dashboard
    :param driver: The webdriver object to use
    :param timeout: The time to wait for the page to load
    :return: None
    """
    url = driver.find_element(value='school-applications-nav')\
        .find_element(By.CLASS_NAME, 'colour-resources').get_attribute('href')
    driver.get(url)
    start_time = time.time()
    while True:
        if '/webcal/calendar/' in driver.current_url:
            return
        elif time.time() > start_time + timeout:
            raise TypeError(
                "The URL is not at the specified Sentral dashboard.\n "
                "Please disable headless mode and test the code to ensure "
                "that it is functional. The page may also have failed to "
                "load in 5 secs. You can change the timeout by passing a "
                "value to the timeout arguement"
            )
