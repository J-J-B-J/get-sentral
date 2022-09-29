"""Scrapers for HTML"""
from bs4 import BeautifulSoup


def scrape_timetable(html: str) -> dict:
    """
    Scrape the HTML for the timetable
    :param html: The HTML source code
    :return: The timetable
    """
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
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
                if 'Room' in period.text:
                    class_room = period.find_all('strong')[1].string
                else:
                    class_room = "Unknown"
            except IndexError:
                class_room = "Unknown"
            try:
                if 'with' in period.text:
                    class_teacher = period.find_all('strong')[-1].string
                else:
                    class_teacher = "Unknown"
            except IndexError:
                class_teacher = "Unknown"
            colour = str(period.find('div').attrs['style'])[-8:-1]
            class_ = {
                "subject": class_name,
                "room": class_room,
                "teacher": class_teacher,
                "colour": colour
            }
        class_number = period.find('th').string
        data[class_number] = class_
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
        try:
            if notice_date[5].split(':')[1][-2:] == 'pm' and hour % 12 > 0:
                hour += 12
        except:
            pass
        notice_date_number = (year, month, day, hour, minute)
        notice_date_string = str(notice.find('small').contents[2]).strip()\
            .lstrip('on ')
        notice_content = ""
        for tag in notice.find_all('p'):
            notice_content += ' '.join(tag.strings) + '\n'

        notice_data = {
            'title': notice_title,
            'teacher': notice_teacher,
            'date': notice_date_number,
            'date string': notice_date_string,
            'content': notice_content
        }
        data.append(notice_data)
    return data


def scrape_calendar(html: str) -> list:
    """
    Scrape the HTML for the calendar
    :param html: The HTML source code
    :return: The calendar events
    """
    # Fetch the page and create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
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
        for event in events_this_day:
            event_obj = {}
            if 'class' not in event.attrs.keys():
                continue
            event_obj['name'] = event.text.replace('Events:', '').strip()
            event_obj['flag'] = event.attrs.get('data-cat-event', '').replace(
                '_', ' ').title()
            event_obj['date'] = day.find('div', class_='center').text
            time = event.find('span', 'tool-tip-time')
            new_name = event_obj['name'].split(' - ')
            x = 0
            for section in new_name:
                if not section.strip()[0].isnumeric():
                    break
                x += 1
            event_obj['name'] = ' - '.join(new_name[x:])
            if time:
                event_obj['date'] += ' ' + time.text
            data.append(event_obj)
    return data
