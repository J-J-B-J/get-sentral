"""Scrapers for HTML"""
from bs4 import BeautifulSoup


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
            colour = str(period.find('div').attrs['style'])[-8:-1]
            class_ = {
                "subject": class_name,
                "room": class_room,
                "teacher": class_teacher,
                "colour": colour
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
