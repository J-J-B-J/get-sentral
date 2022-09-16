"""A function to get the timetable for the current week"""
import datetime
from json import load
import time
import string
import random

import scrapers 
import webdriver
import credentials as creds

print('Created by SuperHarmony910 and J-J-B-J')


def stringgen(length):
    """Generate a random string"""
    letters = string.ascii_lowercase  # define the lower case string
    # define the condition for random.choice() method
    result = ''.join((random.choice(letters)) for _ in range(length))
    return result


def get_timetable(usr: str = None, pwd: str = None, url: str = None,
                  debug: bool = None, timeout: int = 5):
    """Get the timetable for the current week"""
    data = {}

    # Get credentials
    debug, usr, pwd, url = creds.get(debug, usr, pwd, url)

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
    timetable = scrapers.scrape_timetable(driver.page_source)
    for x, y in timetable.items():
        data[x] = y

    if debug:
        print("Navigating to calendar")
    webdriver.go_to_calendar(driver, timeout * 2)

    if debug:
        print("Scraping Calendar")
    calendar = scrapers.scrape_calendar(driver.page_source)
    for x, y in calendar.items():
        data[x] = y

    return data


def __print_colour(text: any, hex_code: str):
    """Print text in a colour represented by a hex code"""
    hex_code = hex_code.upper().lstrip("#")
    closest_colour = '30'
    closest_number = 16666651  # The greatest number possible for a difference
    # between two hex codes, plus one
    hexes = [
        '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0A', '0B',
        '0C', '0D', '0E', '0F', '10', '11', '12', '13', '14', '15', '16', '17',
        '18', '19', '1A', '1B', '1C', '1D', '1E', '1F', '20', '21', '22', '23',
        '24', '25', '26', '27', '28', '29', '2A', '2B', '2C', '2D', '2E', '2F',
        '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
        '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45', '46', '47',
        '48', '49', '4A', '4B', '4C', '4D', '4E', '4F', '50', '51', '52', '53',
        '54', '55', '56', '57', '58', '59', '5A', '5B', '5C', '5D', '5E', '5F',
        '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '6A', '6B',
        '6C', '6D', '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
        '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81', '82', '83',
        '84', '85', '86', '87', '88', '89', '8A', '8B', '8C', '8D', '8E', '8F',
        '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '9A', '9B',
        '9C', '9D', '9E', '9F', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7',
        'A8', 'A9', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
        'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD', 'BE', 'BF',
        'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'CA', 'CB',
        'CC', 'CD', 'CE', 'CF', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7',
        'D8', 'D9', 'DA', 'DB', 'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3',
        'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
        'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'FA', 'FB',
        'FC', 'FD', 'FE', 'FF'
    ]
    colours = (
        '000000',  # Black
        'FF7F7F',  # Red
        '85EE88',  # Green
        'FFF884',  # Yellow
        '84E6DD',  # Blue
        'BF7FFF',  # Purple
        'CEFEFD',  # Cyan
        'EEEEEE',  # White
    )
    for colour in colours:
        diff = 0
        for x in range(0, 6, 2):
            diff += abs(
                hexes.index(hex_code[x:x+2]) - hexes.index(colour[x:x+2])
            )
        if diff < closest_number:
            closest_colour = str(colours.index(colour) + 30)
            closest_number = diff
    print('\x1b[0;' + closest_colour + 'm' + str(text) + '\033[0;0m')


if __name__ == "__main__":
    timetable = get_timetable()

    print("\n\nCLASSES\n")
    for my_period, my_class in timetable['classes'].items():
        if my_class:
            print(f'{my_period}: ', end='')
            __print_colour(
                f"{my_class['subject']} in {my_class['room']}"
                f" with {my_class['teacher']}",
                my_class['colour']
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

    print("\nEVENTS\n")
    for my_event in timetable['events']:
        print(my_event['date'] + ': ' + my_event['name'].upper())
        if my_event['flag']:
            print("Flag: " + my_event['flag'])
        print()
