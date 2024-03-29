"""Print out your details from Sentral"""
import SentralTimetable
from SentralTimetable import get_timetable, objects
import datetime


def __print_colour(text: any, hex_code: str):
    """Print text in a colour represented by a hex code"""
    hex_code = hex_code.upper().lstrip("#")
    closest_colour = '30'
    closest_number = 16666651  # The greatest number possible for a difference
    # between two hex codes, plus one
    hex_system = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                  'C', 'D', 'E', 'F']
    # Sets 'hexes' to ['00', '01', ... '09', '0A', ... '0F', '10', ... 'FF']
    hexes = [a + b for a in hex_system for b in hex_system]

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


def main():
    """The main function"""
    timetable = get_timetable()

    MONTHS = [
        "",
        "Janurary", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]

    print("\n\nCLASSES\n")
    for day in timetable.days:
        print(f"{day.date.dy} {MONTHS[day.date.mth]} {day.date.yr}")
        for period in day.classes:
            if type(period) == objects.Period:
                __print_colour(
                    f"Period {period.period}: {period.subject} in {period.room} "
                      f"with {period.teacher}",
                    period.colour.hex
                )
            else:
                print(f"Period {period.period}")
        print()

    print("\n\nNOTICES\n")
    for notice in timetable.notices:
        print(notice.title.upper())
        print('-' * len(notice.title))
        print(f"By {notice.teacher} on {notice.date}")
        print('-' * len(notice.title))
        if notice.attachments:
            print("Attachments:")
            for attachment in notice.attachments:
                print(f" - \"{attachment.name}\": {attachment.url}")
        print(notice.content + '\n')

    print("\nEVENTS\n")
    for event in timetable.events:
        print(str(event.date), end=': ')

        if event.type_ == 'event':
            print('\x1b[0;32m', end='')
        elif event.type_ == 'assessment':
            print('\x1b[0;31m', end='')

        print(event.title.upper() + '\033[0;0m')
        if event.flag:
            print("Flag: ", end='')
            try:
                # Print with colour
                print(f"\x1b[0;{int(event.flag.split()[1]) + 24}m", end='')
            except ValueError:
                pass
            print(event.flag + '\033[0;0m')
        print()

    with timetable.user.journal as journal:
        if journal == SentralTimetable.JournalUnavailableError:
            journal = "Today is a weekend/holiday. You cannot access your " \
                      "journal."
        elif journal == "":
            journal = "You do not have a journal entry for today."

    print("\n\nME\n")
    print(f"Name: {timetable.user.name}")
    print(f"Number: {timetable.user.number}")
    print(f"School: {timetable.user.school}")
    print(f"\nBarcode:\n\n{timetable.user.barcode}")
    print(f"\nJournal:\n{journal}")

    reports = '\n'.join([str(report) for report in timetable.user.reports])
    print(f"\nReports:\n{reports}")


if __name__ == "__main__":
    main()
