"""
Run this as an example to test out the code. If you have built and installed
the package, you should be able to use it in another directory.
"""
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

    print("\n\nCLASSES\n")
    for class_ in timetable.classes:
        if type(class_) == objects.Period:
            class_: objects.Period
            print(f'{class_.period}: ', end='')
            __print_colour(
                f"{class_.subject} in {class_.room}"
                f" with {class_.teacher}",
                class_.colour.hex
            )
        elif type(class_) == objects.EmptyPeriod:
            class_: objects.EmptyPeriod
            print(f"{class_.period}: Empty")

    print("\n\nNOTICES\n")
    for notice in timetable.notices:
        print(notice.title.upper())
        print('-' * len(notice.title))
        print(f"By {notice.teacher} on {notice.date}")
        print('-' * len(notice.title))
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


if __name__ == "__main__":
    main()
