"""Scrapers for HTML"""
from .objects import *

from bs4 import BeautifulSoup
import datetime
from BarcodeGenerator import generate_barcode


MONTHS_LONG = [
    "",
    "January",   "February", "March",    "April",
    "May",       "June",     "July",     "August",
    "September", "October",  "November", "December"
]

MONTHS_SHORT = [
    "",
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]


def scrape_timetable(html: str) -> list[Period or EmptyPeriod]:
    """
    Scrape the HTML for the timetable
    :param html: The HTML source code
    :return: The timetable
    """
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    try:
        timetable_periods = soup.find(class_="timetable table").find_all('tr')
    except AttributeError:
        return data
    for period in timetable_periods:
        class_number = str(period.find('th').string)
        if 'inactive' in period.find('td')['class']:
            class_ = EmptyPeriod(class_number)
        else:
            try:
                class_name = str(period.find_all('strong')[0].string)
            except IndexError:
                class_name = "Unknown"
            try:
                if 'Room' in period.text:
                    class_room = str(period.find_all('strong')[1].string)
                else:
                    class_room = "Unknown"
            except IndexError:
                class_room = "Unknown"
            try:
                if 'with' in period.text:
                    class_teacher = str(period.find_all('strong')[-1].string)
                else:
                    class_teacher = "Unknown"
            except IndexError:
                class_teacher = "Unknown"
            colour = str(period.find('div').attrs['style'])[-8:-1]
            class_ = Period(
                class_number,
                class_name,
                class_room,
                class_teacher,
                Colour(colour)
            )
        data.append(class_)
    return data


def scrape_notices(html: str) -> list:
    """
    Scrape the HTML for the notices
    :param html: The HTML source code
    :return: Notices
    """
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    data = []
    notices = soup.find_all(class_='notice-wrap')
    for notice in notices:
        notice_title = str(notice.find('h4').string)
        notice_teacher = str(notice.find_all('strong')[1].string.strip())
        notice_date = \
            str(notice.find('small').contents[2]).strip().lstrip('on ').split()
        try:
            day = int(notice_date[1])
        except ValueError:
            day = 1
        try:
            month = MONTHS_LONG.index(notice_date[2])
        except ValueError:
            month = 1
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
        try:
            if notice_date[5].split(':')[1][-2:] == 'pm' and hour % 12 > 0:
                hour += 12
        except ValueError:
            pass

        notice_date = Date(year, month, day, hour, minute)

        notice_content = ""
        for tag in notice.find_all('p'):
            notice_content += ' '.join(tag.strings) + '\n'

        notice_data = Notice(
            notice_title,
            notice_teacher,
            notice_date,
            notice_content
        )
        data.append(notice_data)
    return data


def scrape_user(html: str) -> User:
    """
    Scrape the user data
    :param html: The HTML source code
    :return: The user data
    """
    soup = BeautifulSoup(html, 'html.parser')
    try:
        school_div = soup.find('h1')
        school = str(school_div.text)
        subtext = str(school_div.find('span').text)
        school = school.replace(subtext, '').strip()
    except AttributeError:
        school = "Unknown"

    student_div = soup.find(class_='student-login')
    try:
        name = str(student_div.find('span').text.title())
    except AttributeError:
        name = "Unknown"
    try:
        number = int(student_div.find('small').text)
    except AttributeError:
        number = 0
    except ValueError:
        number = 0
    barcode = generate_barcode(number)

    return User(name, school, number, barcode)


def scrape_calendar(html: str) -> list:
    """
    Scrape the HTML for the calendar
    :param html: The HTML source code
    :return: The calendar events
    """
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    try:
        year = int(soup.find(class_='padding-x color_primary_text').text.
                   split()[-1])
    except ValueError:
        year = 0
    data = []
    calendar = soup.find('table', class_='calendar')
    days = calendar.find_all('td', id=True)
    for day in days:
        events_div = day.find('div', class_='calendar-eventdata')
        if events_div:
            events_this_day = events_div.find_all('div')
        else:
            # There are no events on this date
            events_this_day = []

        date_text = str(day.find('div', class_='center').text).split()
        try:
            month = MONTHS_SHORT.index(date_text[0])
        except ValueError:
            month = 1
        try:
            day = int(date_text[1])
        except ValueError:
            day = 1

        for event in events_this_day:
            if 'class' not in event.attrs.keys():
                continue
            event_title = str(event.text.replace('Events:', '')
                              .replace('Assessment: ', '').strip())
            event_flag = str(event.attrs.get('data-cat-event', '').replace(
                '_', ' ').title())
            time = event.find('span', 'tool-tip-time')
            new_name = event_title.split(' - ')
            x = 0
            for section in new_name:
                if not section.strip()[0].isnumeric():
                    break
                x += 1
            event_title = ' - '.join(new_name[x:])
            if time:
                time_text = str(time.text).split()
                if len(time_text[0].split(":")) == 2:
                    try:
                        start_hour = int(time_text[0].split(':')[0])
                    except ValueError:
                        start_hour = 0
                    try:
                        start_minute = int(time_text[0].split(':')[1][:-2])
                    except ValueError:
                        start_minute = 0
                    try:
                        if time_text[0].split(':')[1][-2:] == 'pm' and \
                                start_hour % 12 > 0:
                            start_hour += 12
                    except ValueError:
                        pass
                else:
                    try:
                        start_hour = int(time_text[0][:-2])
                    except ValueError:
                        start_hour = 0
                    try:
                        if time_text[0][-2:] == 'pm' and start_hour % 12 > 0:
                            start_hour += 12
                    except ValueError:
                        pass
                    start_minute = 0
                if len(time_text[2].split(":")) == 2:
                    try:
                        end_hour = int(time_text[2].split(':')[0])
                    except ValueError:
                        end_hour = 0
                    try:
                        end_minute = int(time_text[2].split(':')[1][:-2])
                    except ValueError:
                        end_minute = 0
                    try:
                        if time_text[2].split(':')[1][-2:] == 'pm' and \
                                end_hour % 12 > 0:
                            end_hour += 12
                    except ValueError:
                        pass
                else:
                    try:
                        end_hour = int(time_text[2][:-2])
                    except ValueError:
                        end_hour = 0
                    try:
                        if time_text[2][-2:] == 'pm' and end_hour % 12 > 0:
                            end_hour += 12
                    except ValueError:
                        pass
                    end_minute = 0
                event_date = DateRange(
                    year, month, day,
                    start_hour, start_minute,
                    end_hour, end_minute
                )
            else:
                event_date = Date(year, month, day)

            event_type = "UNKNOWN"
            if 'green' in event.attrs['class']:
                event_type = "event"
            elif 'red' in event.attrs['class']:
                event_type = "assessment"
            data.append(Event(
                event_title,
                event_date,
                event_flag,
                event_type
            ))
    return data
