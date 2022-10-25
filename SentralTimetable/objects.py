"""Classes to manage the objects in the timetable."""


# Yes I know it is the Australian spelling. Deal with it.
class Colour:
    """A class to manage a colour."""
    def __init__(self, hex_code: str):
        """Initialise the class."""
        self.hex = hex_code

        if len(self.hex) != 7:
            raise ValueError("Invalid colour")
        if self.hex[0] != "#":
            raise ValueError("Invalid colour")
        try:
            self.red = int("0x" + self.hex[1:3], 0)
            self.green = int("0x" + self.hex[3:5], 0)
            self.blue = int("0x" + self.hex[5:7], 0)
        except ValueError:
            raise ValueError("Invalid colour")
        self.r, self.g, self.b = self.red, self.green, self.blue
        self.rgb = (self.red, self.green, self.blue)

    def __str__(self):
        """Return a string representation of the colour."""
        return self.hex

    def __repr__(self):
        """Return a string representation of the colour."""
        return f"Colour({self.hex})"


class EmptyPeriod:
    """A class to manage an empty period."""

    def __init__(self, period: str):
        self.period = period

    def __str__(self):
        return f"Empty Period {self.period}"

    def __repr__(self):
        return f"EmptyPeriod({self.period})"


class Period(EmptyPeriod):
    """A class to manage a period."""

    def __init__(self, period: str, subject: str, room: str, teacher: str,
                 colour: Colour):
        super().__init__(period)
        self.subject = subject
        self.room = room
        self.teacher = teacher
        self.colour = colour

    def __str__(self):
        return f"Period {self.period}: {self.subject} in {self.room} with " \
               f"{self.teacher}"

    def __repr__(self):
        return f"Period({self.period}, {self.subject}, {self.room}, " \
               f"{self.teacher}, {self.colour})"


class Date:
    """A class to manage a date."""

    def __init__(self, year: int, month: int, day: int, hour: int = 0,
                 minute: int = 0):
        self.year = self.yr = year
        self.month = self.mth = month
        self.day = self.dy = day
        self.hour = self.hr = hour
        self.minute = self.mnt = minute

        if self.year % 4 == 0:
            feb = 29
        else:
            feb = 28
        days_in_months = [0, 31, feb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if self.year < 0:
            raise ValueError("Invalid year")
        if self.month < 1 or self.month > 12:
            raise ValueError("Invalid month")
        if self.day < 1 or self.day > days_in_months[self.month]:
            raise ValueError("Invalid day")
        if self.hour < 0 or self.hour > 23:
            raise ValueError("Invalid hour")
        if self.minute < 0 or self.minute > 59:
            raise ValueError("Invalid minute")

    def __str__(self):
        if self.hour != 0 or self.minute != 0:
            return f"{self.day}/{self.month}/{self.year} {self.hour}:" \
                   f"{str(self.minute).rjust(2, '0')}"
        else:
            return f"{self.day}/{self.month}/{self.year}"

    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day}, {self.hour}, " \
               f"{str(self.minute).rjust(2, '0')})"


class DateRange:
    """A class to manage a date that has a range but is on the same day."""

    def __init__(self, year: int, month: int, day: int, start_hour: int,
                 start_minute: int, end_hour: int, end_minute: int):
        self.year = self.yr = year
        self.month = self.mth = month
        self.day = self.dy = day
        self.start_hour = self.s_hr = start_hour
        self.start_minute = self.s_mnt = start_minute
        self.end_hour = self.e_hr = end_hour
        self.end_minute = self.e_mnt = end_minute

    def __str__(self):
        return f"{self.day}/{self.month}/{self.year} {self.start_hour}:" \
               f"{str(self.start_minute).rjust(2, '0')} to {self.end_hour}:" \
               f"{str(self.end_minute).rjust(2, '0')}"

    def __repr__(self):
        return f"DateRange({self.year}, {self.month}, {self.day}, " \
               f"{self.start_hour}, {self.start_minute}, {self.end_hour}, " \
               f"{self.end_minute})"


class Notice:
    """A class to manage a notice."""

    def __init__(self, title: str, teacher: str, date: Date, content: str):
        self.title = title
        self.teacher = teacher
        self.date = date
        self.content = content

    def __str__(self):
        return f"{self.title} by {self.teacher} on {self.date}"

    def __repr__(self):
        return f"Notice({self.title}, {self.teacher}, {self.date})"


class Event:
    """A class to manage an event."""

    def __init__(self, title: str, date: Date or DateRange, flag: str,
                 type_: str):
        self.title = title
        self.date = date
        self.flag = flag
        self.type_ = type_

    def __str__(self):
        return f"{self.title} ({self.flag}, {self.type_}) on {self.date}"

    def __repr__(self):
        return f"Event({self.title} on {self.date})"


class User:
    """A class to manage the user details"""

    def __init__(self, name: str, school: str, number: int, barcode: str):
        self.name = name
        self.school = school
        self.number = number
        self.barcode = barcode

    def __str__(self):
        return f"{self.name} ({self.school}, {self.number})\n{self.barcode}"

    def __repr__(self):
        return f"User({self.name}, {self.school}, {self.number}, " \
               f"{self.barcode})"


class Sentral:
    """One class to rule them all... or at least contain the others"""

    def __init__(self, classes: list[Period or EmptyPeriod],
                 notices: list[Notice], events: list[Event], user: User):
        self.classes = classes
        self.notices = notices
        self.events = events
        self.user = user

    def __str__(self):
        return f"Sentral({self.classes}, {self.notices}, {self.events}, " \
               f"{self.user})"

    def __repr__(self):
        return f"Sentral({self.classes}, {self.notices}, {self.events}, " \
               f"{self.user})"
