"""Scrapers for HTML"""
# Standard library imports
import datetime

# Third party imports
from BarcodeGenerator import generate_barcode
from bs4 import BeautifulSoup
import datetime

# Local imports
from .objects import *

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

class JournalUnavailableError(Exception):
    """The journal for today is not available"""
    pass


def scrape_timetable(html: str) -> list[SchoolDay]:
    """
    Scrape the HTML for the timetable
    :param html: The HTML source code
    :return: The timetable
    """
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    # Find the table containing the timetable and split it by weeks
    timetable = soup.find(class_='timetable table')
    weeks = [
        BeautifulSoup(x, 'html.parser')  # A BeautifulSoup object for each week
        for x in str(timetable).split('<!-- Spacers -->')
    ][:-1]  # Remove the last item, which is spacers at the end of the table

    if not weeks:
        return data

    # Find the number of days in a week
    date_cells = weeks[0].find_all('th', class_='timetable-date')
    days_in_week = int(len(date_cells) / 2)  # Divide by two because the day of
    # the week, e.g. "Monday", and the date, e.g. "1/1/2022" cells both have
    # the class "timetable-date" :(

    # Create the objects
    for week in weeks:
        days = {}

        # Get the dates
        date_cells = week.find_all('th', class_='timetable-date')\
            [days_in_week:]
        for date_cell in date_cells:  # Date format is "DD/MM/YYYY"
            date = date_cell.text.split("/")
            try:
                day = int(date[0])
            except ValueError:
                day = 1
            try:
                month = int(date[1])
            except ValueError:
                month = 1
            try:
                year = int(date[2])
            except ValueError:
                year = 0
            days[Date(year, month, day)] = []

        # Get the periods
        rows = BeautifulSoup(
            str(week).split("<!-- Periods")[1],
            'html.parser'
        ).find_all('tr')  # Ignore the header rows
        for row in rows:
            row_name = row.find('th').string.strip()
            row_periods = row.find_all('td', class_='timetable-dayperiod')
            for i, period in enumerate(row_periods):
                if 'class="inactive' in str(period):
                    class_ = EmptyPeriod(row_name)
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
                        row_name,
                        class_name,
                        class_room,
                        class_teacher,
                        Colour(colour)
                    )
                days[list(days.keys())[i]].append(class_)

        # Convert the dictionary to SchoolDay objects
        for date, periods in days.items():
            data.append(SchoolDay(periods, date))

    return data


def scrape_notices(html: str, url: str) -> list:
    """
    Scrape the HTML for the notices
    :param url: The URL of the page
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

        base_url = "/".join(url.split('/')[0:3])

        attachment_div = notice.find(class_='dropdown-menu')
        attachments = []
        if attachment_div is not None:
            for attachment in attachment_div.find_all('li'):
                attachment_name = str(attachment.find('a').string).strip()
                attachment_url = base_url + str(attachment.find('a')['href'])
                attachments.append(Attachment(attachment_name, attachment_url))

        notice_data = Notice(
            notice_title,
            notice_teacher,
            notice_date,
            notice_content,
            attachments
        )
        data.append(notice_data)
    return data


def scrape_user(html_home: str, html_reporting: str, url: str) -> User:
    """
    Scrape the user data
    :param html_home: The HTML source code for the Sentral home page
    :param html_reporting: The HTML source code for the Sentral reporting page
    :param url: The URL of the home page
    :return: The user data
    """
    soup_home = BeautifulSoup(html_home, 'html.parser')
    try:
        school_div = soup_home.find('h1')
        school = str(school_div.text)
        subtext = str(school_div.find('span').text)
        school = school.replace(subtext, '').strip()
    except AttributeError:
        school = "Unknown"

    student_div = soup_home.find(class_='student-login')
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

    try:
        journal_form = soup_home.find_all(class_='span3')[1].find('form')
        journal_text_box = journal_form.find(class_='editable')
    except AttributeError:
        journal = JournalUnavailableError
    except IndexError:
        journal = JournalUnavailableError
    else:
        if journal_text_box is None:
            journal = ""
        else:
            journal = ""
            # Get the text from all the <p> tags. This is necessary to stop the
            # text inside the button from being scraped
            for tag in journal_form.find_all('p'):
                journal += ' '.join(tag.strings) + '\n'
            journal = journal.rstrip()  # Remove the trailing newline

    soup_reporting = BeautifulSoup(html_reporting, 'html.parser')

    reports = []
    for report in reversed(soup_reporting.find_all('tr')[1:]):  # The rows
        # excluding the header, in reverse order
        report_name = str(report.find('td').text)
        report_url = '/'.join(url.split('/')[:3])+str(report.find('a')['href'])

        date = str(report.find_all('td')[1].text)
        try:
            day = int(date.split('/')[0])
        except ValueError:
            day = 1
        try:
            month = int(date.split('/')[1])
        except ValueError:
            month = 1
        try:
            year = int(date.split('/')[2].split(' ')[0])
        except ValueError:
            year = 0
        try:
            hour = int(date.split(' ')[1].split(':')[0])
        except ValueError:
            hour = 0
        try:
            minute = int(date.split(' ')[1].split(':')[1])
        except ValueError:
            minute = 0

        report_date = Date(year, month, day, hour, minute)

        reports.append(Report(report_name, report_url, report_date))

    return User(name, school, number, barcode, journal, reports)


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
