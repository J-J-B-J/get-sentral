"""The app for get-sentral."""
# Standard library imports
from calendar import Calendar
import datetime
from functools import partial
import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter.messagebox import *

# Local imports
import SentralTimetable


class App:
    """Overall class to manage the app."""

    def __init__(self):
        """Initialize the app."""
        self.window = tk.Tk()
        self.window.title("Sentral")
        self.window.geometry("500x500")
        self.window.iconphoto(True, tk.PhotoImage(file='docs/img/icon.png'))
        self.window.bind("<Command-r>", self.reload)

        self.create_buttons()
        self.section_objects = []
        self.data = SentralTimetable.Sentral(
            [],
            [],
            [],
            SentralTimetable.User("", "", 0, "")
        )

        self.notice_range_start = 0
        self.event_range_start = -1

        try:
            with open("App_Data.txt", "r") as file:
                self.username = file.readline().strip()
                self.password = file.readline().strip()
                self.url = file.readline().strip()
        except Exception:
            self.username = ""
            self.password = ""
            self.url = ""

        if not self.username or not self.password or not self.url:
            self.settings()
        else:
            self.reload()

    def create_buttons(self):
        """Create the buttons for the top of the app"""
        self.frm_button = tk.Frame(self.window, width=500)
        self.frm_button.pack()

        def create_button(text: str, bind_fn: callable):
            """Create a single button"""
            btn = tk.Button(
                self.frm_button,
                text=text,
                width=10
            )
            btn.pack(side=tk.LEFT)
            btn.bind("<Button-1>", bind_fn)
            return btn

        self.btn_timetable = create_button(
            "Timetable",
            self.timetable
        )
        self.btn_notices = create_button(
            "Notices",
            self.notices
        )
        self.btn_events = create_button(
            "Events",
            self.events
        )
        self.btn_me = create_button(
            "Me",
            self.me
        )
        self.btn_settings = create_button(
            "Settings",
            self.settings
        )
        self.btn_reload = tk.Button(
            self.frm_button,
            text="↻",
            width=3
        )
        self.btn_reload.pack()
        self.btn_reload.bind("<Button-1>", self.reload)

    def destroy_section_objects(self):
        """Destroy all the objects in the section_objects list."""
        for object_ in self.section_objects:
            object_.destroy()
        self.section_objects = []

    def create_title(self, title: str):
        """Create a title for the page."""
        lbl_title = tk.Label(
            self.window,
            text=title,
            font=("Arial", 20)
        )
        self.section_objects.append(lbl_title)
        lbl_title.pack(side=tk.TOP)
        return lbl_title

    def reload(self, *args):
        """Reload the data"""
        self.window.unbind("<Command-r>")
        self.destroy_section_objects()
        self.frm_button.destroy()
        self.create_title("Loading...")

        progressbar = ttk.Progressbar(
            self.window,
            orient='horizontal',
            length=300,
            mode='determinate'
        )
        self.section_objects.append(progressbar)
        progressbar.pack()
        progressbar.start(280)

        def sentral(*args):
            """Get the timetable"""
            self.data = SentralTimetable.get_timetable(
                debug=False,
                timeout=30,
                usr=self.username,
                pwd=self.password,
                url=self.url
            )

        sentral_thread = Thread(target=sentral)
        sentral_thread.start()

        def reload(*args):
            """Reload the 'reload' window"""
            progressbar.start()
            if not sentral_thread.is_alive():
                self.destroy_section_objects()
                self.create_buttons()
                self.window.bind("<Command-r>", self.reload)
                self.timetable()
            else:
                self.window.after(200, reload)

        reload()

        self.window.mainloop()

    def timetable(self, *args):
        """The 'timetable' page"""
        self.destroy_section_objects()
        self.create_title("Timetable")

        if not self.data.classes:
            lbl_no_notices = tk.Label(
                self.window,
                text="No classes found."
            )
            self.section_objects.append(lbl_no_notices)
            lbl_no_notices.pack()

        frm_timetable = tk.Frame(self.window, width=500, height=450)
        self.section_objects.append(frm_timetable)
        frm_timetable.pack()

        periods = []
        for period in self.data.classes:
            frm_period = tk.Frame(frm_timetable, width=500, height=50)
            self.section_objects.append(frm_period)
            frm_period.pack()

            lbl_period_number = tk.Label(
                frm_period,
                text=period.period,
                width=5,
                height=2
            )
            self.section_objects.append(lbl_period_number)
            lbl_period_number.pack(side=tk.LEFT)
            if type(period) == SentralTimetable.Period:
                lbl_period_name = tk.Label(
                    frm_period,
                    text=f"{period.subject} in {period.room} with "
                         f"{period.teacher}",
                    background=period.colour.hex,
                    width=40,
                    height=2,
                    wraplength=390,
                    borderwidth=3,
                    relief="raised"
                )
            else:
                lbl_period_name = tk.Label(
                    frm_period,
                    width=40,
                    height=2
                )
            self.section_objects.append(lbl_period_name)
            lbl_period_name.pack(side=tk.LEFT)

            periods.append(frm_period)

    def notices(self, *args):
        """The 'notices' page"""
        self.destroy_section_objects()
        self.create_title("Notices")

        if not self.data.notices:
            lbl_no_notices = tk.Label(
                self.window,
                text="No daily notices recorded for today. "
                     "Please check back later."
            )
            self.section_objects.append(lbl_no_notices)
            lbl_no_notices.pack()

        frm_notices = tk.Frame(self.window, width=500, height=450)
        self.section_objects.append(frm_notices)
        frm_notices.pack()

        def increase_range(*args):
            """Increase the range of notices shown"""
            self.notice_range_start += 5
            self.notices()

        def decrease_range(*args):
            """Decrease the range of notices shown"""
            self.notice_range_start -= 5
            self.notices()

        def open_notice(notice: SentralTimetable.Notice, event: tk.Event):
            """Show the detail view for a notice"""
            notice_window = tk.Tk()
            notice_window.title('Notice')
            notice_window.geometry('500x150')
            notice_window.focus_set()
            notice_window.bind(
                "<Escape>",
                lambda *args: notice_window.destroy()
            )

            lbl_title = tk.Label(
                notice_window,
                text=notice.title,
                font=("Arial", 20)
            )
            lbl_title.pack(side=tk.TOP)

            lbl_date = tk.Label(
                notice_window,
                text=f"By {notice.teacher} on "
                     f"{notice.date.day}/{notice.date.month}/"
                     f"{notice.date.year} at {notice.date.hour}:"
                     f"{notice.date.minute}"
            )
            lbl_date.pack(side=tk.TOP)

            lbl_content = tk.Label(
                notice_window,
                text=notice.content,
                wraplength=490
            )
            lbl_content.pack(side=tk.TOP)

            notice_window.mainloop()

        for notice in self.data.notices[self.notice_range_start:self.notice_range_start + 5]:
            frm_notice = tk.Frame(frm_notices, width=500, height=50)
            self.section_objects.append(frm_notice)
            frm_notice.pack()

            lbl_notice_title = tk.Label(
                frm_notice,
                text=notice.title,
                width=50,
                height=2,
                wraplength=390,
                borderwidth=3,
                relief="raised"
            )
            self.section_objects.append(lbl_notice_title)
            lbl_notice_title.pack(side=tk.LEFT)
            lbl_notice_title.bind(
                "<Button-1>",
                partial(open_notice, notice)
            )

        btn_increase_range = tk.Button(
            frm_notices,
            text=">",
            width=10
        )
        self.section_objects.append(btn_increase_range)
        btn_increase_range.pack(side=tk.RIGHT)
        if self.notice_range_start + 5 < len(self.data.notices):
            btn_increase_range.bind("<Button-1>", increase_range)
        else:
            btn_increase_range.config(state=tk.DISABLED)

        btn_decrease_range = tk.Button(
            frm_notices,
            text="<",
            width=10
        )
        self.section_objects.append(btn_decrease_range)
        btn_decrease_range.pack(side=tk.LEFT)
        if self.notice_range_start > 0:
            btn_decrease_range.bind("<Button-1>", decrease_range)
        else:
            btn_decrease_range.config(state=tk.DISABLED)

    def events(self, *args):
        """The 'timetable' page"""
        self.destroy_section_objects()
        self.create_title("Events")

        if not self.data.events:
            lbl_no_events = tk.Label(
                self.window,
                text="No events found."
            )
            self.section_objects.append(lbl_no_events)
            lbl_no_events.pack()
            return

        frm_calendar = tk.Frame(self.window, width=500, height=450)
        self.section_objects.append(frm_calendar)
        frm_calendar.pack()

        start_month = self.data.events[0].date.month
        start_year = self.data.events[0].date.year
        end_month = self.data.events[-1].date.month
        end_year = self.data.events[-1].date.year

        cal = Calendar(6)
        months = [
            cal.monthdatescalendar(y, m)
            for m in range(start_month, end_month + 1)
            for y in range(start_year, end_year + 1)
        ]

        if self.event_range_start == -1:
            if datetime.date.today().month in \
                    [m for m in range(start_month, end_month + 1)]:
                self.event_range_start = datetime.date.today().month - \
                                         start_month
        month = months[self.event_range_start]

        lbl_month = tk.Label(
            frm_calendar,
            text=month[2][0].strftime("%B %Y"),
            font=("Arial", 20),
            width=50,
            height=2
        )
        self.section_objects.append(lbl_month)
        lbl_month.pack()

        def increase_range(*args):
            """Increase the range of events shown"""
            self.event_range_start += 1
            self.events()

        def decrease_range(*args):
            """Decrease the range of events shown"""
            self.event_range_start -= 1
            self.events()

        def open_event(event: SentralTimetable.Event, tk_event: tk.Event):
            """Show the detail view for an event"""
            event_window = tk.Tk()
            event_window.title('Event')
            event_window.geometry('500x150')
            event_window.focus_set()
            event_window.bind(
                "<Escape>",
                lambda *args: event_window.destroy()
            )

            lbl_title = tk.Label(
                event_window,
                text=event.title,
                font=("Arial", 20),
                wraplength=490
            )
            lbl_title.pack(side=tk.TOP)

            if type(event.date) == SentralTimetable.Date:
                if event.date.hour == 0 and event.date.minute == 0:
                    lbl_date = tk.Label(
                        event_window,
                        text=f"On {event.date.day}/{event.date.month}/"
                             f"{event.date.year}"
                    )
                else:
                    lbl_date = tk.Label(
                        event_window,
                        text=f"On {event.date.day}/{event.date.month}/"
                             f"{event.date.year} at {event.date.hour}:"
                             f"{str(event.date.minute).rjust(2, '0')}"
                    )
            else:
                lbl_date = tk.Label(
                    event_window,
                    text=f"On {event.date.day}/{event.date.month}/"
                         f"{event.date.year} from {event.date.start_hour}:"
                         f"{str(event.date.start_minute).rjust(2, '0')} to "
                         f"{event.date.end_hour}:"
                         f"{str(event.date.end_minute).rjust(2, '0')}"
                )
            lbl_date.pack(side=tk.TOP)

            if event.flag:
                lbl_flag = tk.Label(
                    event_window,
                    text=f"Flag: {event.flag}",
                    wraplength=490
                )
                lbl_flag.pack(side=tk.TOP)

            lbl_type = tk.Label(
                event_window,
                text=f"Type: {event.type_}",
                wraplength=490
            )
            lbl_type.pack(side=tk.TOP)

            event_window.mainloop()

        def open_day(day: datetime.date, tk_event: tk.Event):
            """Show the events for a day"""
            day_window = tk.Tk()
            day_window.title(day.strftime("%A %d %B %Y"))
            day_window.geometry('500x150')
            day_window.focus_set()
            day_window.bind(
                "<Escape>",
                lambda *args: day_window.destroy()
            )

            lbl_title = tk.Label(
                day_window,
                text=f"Events on {day.day}/{day.month}/{day.year}",
                font=("Arial", 20)
            )
            lbl_title.pack(side=tk.TOP)

            for event in self.data.events:
                if (event.date.dy, event.date.mth, event.date.yr) == \
                        (day.day, day.month, day.year):
                    lbl_event = tk.Label(
                        day_window,
                        text=event.title,
                        wraplength=490
                    )
                    lbl_event.pack(side=tk.TOP)
                    lbl_event.bind(
                        "<Button-1>",
                        partial(open_event, event)
                    )

            day_window.mainloop()

        frm_days = tk.Frame(frm_calendar, width=500, height=50)
        self.section_objects.append(frm_days)
        frm_days.pack()

        for day in ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]:
            lbl_day = tk.Label(
                frm_days,
                text=day,
                width=4,
                height=2,
                borderwidth=3
            )
            self.section_objects.append(lbl_day)
            lbl_day.pack(side=tk.LEFT)

        for week in month:
            frm_week = tk.Frame(frm_calendar, width=500, height=50)
            self.section_objects.append(frm_week)
            frm_week.pack()

            for day in week:
                lbl_day = tk.Label(
                    frm_week,
                    text=day.day,
                    width=4,
                    height=2,
                    borderwidth=3
                )
                self.section_objects.append(lbl_day)
                lbl_day.pack(side=tk.LEFT)

                if day.month == month[2][0].month:
                    lbl_day.config(relief="groove")
                    lbl_day.bind(
                        "<Button-1>",
                        partial(open_day, day)
                    )
                else:
                    lbl_day.config(state=tk.DISABLED)

                if day.month == datetime.date.today().month and \
                        day.day == datetime.date.today().day:
                    lbl_day.config(font=("Arial", "15", "bold"))

        btn_increase_range = tk.Button(
            frm_calendar,
            text=">",
            width=10
        )
        self.section_objects.append(btn_increase_range)
        btn_increase_range.pack(side=tk.RIGHT)
        if self.event_range_start + 1 < len(months):
            btn_increase_range.bind("<Button-1>", increase_range)
        else:
            btn_increase_range.config(state=tk.DISABLED)

        btn_decrease_range = tk.Button(
            frm_calendar,
            text="<",
            width=10
        )
        self.section_objects.append(btn_decrease_range)
        btn_decrease_range.pack(side=tk.LEFT)
        if self.event_range_start > 0:
            btn_decrease_range.bind("<Button-1>", decrease_range)
        else:
            btn_decrease_range.config(state=tk.DISABLED)

    def me(self, *args):
        """The 'me' page"""
        self.destroy_section_objects()
        self.create_title("Me")

        frm_me = tk.Frame(self.window, width=500, height=500)
        self.section_objects.append(frm_me)
        frm_me.pack()

        lbl_name = tk.Label(
            frm_me,
            text=self.data.user.name,
            font=("Arial", 20)
        )
        self.section_objects.append(lbl_name)
        lbl_name.pack(side=tk.TOP)

        lbl_school = tk.Label(
            frm_me,
            text=self.data.user.school
        )
        self.section_objects.append(lbl_school)
        lbl_school.pack(side=tk.TOP)

        lbl_number = tk.Label(
            frm_me,
            text=self.data.user.number
        )
        self.section_objects.append(lbl_number)
        lbl_number.pack(side=tk.TOP)

        def show_barcode(*args):
            barcode_window = tk.Tk()
            barcode_window.title("Barcode")
            barcode_window.geometry('1100x140')
            barcode_window.focus_set()
            barcode_window.bind(
                "<Escape>",
                lambda *args: barcode_window.destroy()
            )

            lbl_barcode = tk.Label(
                barcode_window,
                text=self.data.user.barcode,
                font=("Arial", 15)
            )
            lbl_barcode.pack()

            barcode_window.mainloop()

        btn_barcode = tk.Button(
            frm_me,
            text="Show barcode",
            width=10
        )
        self.section_objects.append(btn_barcode)
        btn_barcode.pack(side=tk.TOP)
        btn_barcode.bind("<Button-1>", show_barcode)

    def settings(self, *args):
        """The 'settings' page"""
        self.destroy_section_objects()
        self.create_title("Settings")

        frm_settings = tk.Frame(self.window, width=500, height=500)
        self.section_objects.append(frm_settings)
        frm_settings.pack()

        # Create the User details
        lbl_login = tk.Label(
            frm_settings,
            text="Login details",
            fg="grey50",
            anchor=tk.W,
        )
        self.section_objects.append(lbl_login)
        lbl_login.pack(side=tk.TOP, fill=tk.X)

        def create_setting(name: str, initial_text: str, help_text: str):
            """Create a setting"""
            def show_help_window(title: str, text: str, event: tk.Event):
                """Show a window with help text"""
                window = tk.Tk()
                window.title(title)
                window.geometry('250x100')
                window.resizable(False, True)
                window.focus_set()
                window.bind(
                    "<Escape>",
                    lambda *args: window.destroy()
                )

                lbl_text = tk.Label(
                    window,
                    text=text,
                    wraplength=240,
                    justify=tk.LEFT
                )
                lbl_text.pack()

                window.mainloop()

            frm_setting = tk.Frame(frm_settings, width=500, height=50)
            self.section_objects.append(frm_setting)
            frm_setting.pack()

            lbl_setting = tk.Label(
                frm_setting,
                text=name,
                anchor=tk.W,
                width=10
            )
            self.section_objects.append(lbl_setting)
            lbl_setting.pack(side=tk.LEFT)

            btn_setting_help = tk.Button(
                frm_setting,
                text="?",
                width=2
            )
            self.section_objects.append(btn_setting_help)
            btn_setting_help.pack(side=tk.LEFT)
            btn_setting_help.bind(
                "<Button-1>",
                partial(show_help_window, name, help_text)
            )

            if name == "Password":
                ent_setting = tk.Entry(
                    frm_setting,
                    show="*",
                    width=30
                )
            else:
                ent_setting = tk.Entry(
                    frm_setting,
                    width=30
                )

            ent_setting.insert(0, initial_text)
            self.section_objects.append(ent_setting)
            ent_setting.pack(side=tk.RIGHT)

            return ent_setting

        ent_username = create_setting(
            "Username",
            self.username,
            "The username you use to login to Sentral"
        )
        ent_password = create_setting(
            "Password",
            self.password,
            "The password you use to login to Sentral"
        )
        ent_url = create_setting(
            "URL",
            self.url,
            "The URL of your school's Sentral dashboard. Must start with "
            "https:// and end with /portal/dashboard.\nE.g. "
            "https://examplehs.sentral.com.au/portal/dashboard"
        )

        def save_settings(*args):
            """Save the settings"""
            self.username = ent_username.get()
            self.password = ent_password.get()
            self.url = ent_url.get()
            with open("App_Data.txt", "w") as file:
                file.write(f"{self.username}\n{self.password}\n{self.url}")
            if askyesno("Saved", "Save complete. Do you want to reload?"):
                self.reload()

        btn_save = tk.Button(
            frm_settings,
            text="Save",
            width=10
        )
        self.section_objects.append(btn_save)
        btn_save.pack(side=tk.BOTTOM)
        btn_save.bind("<Button-1>", save_settings)

    def run(self):
        """Run the app."""
        self.timetable()
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
