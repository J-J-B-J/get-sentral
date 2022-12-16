"""The app for get-sentral."""
# Standard library imports
from calendar import Calendar
from functools import partial
from PIL import ImageTk, Image
from threading import Thread
from tkinter import ttk
from tkinter.messagebox import *
import datetime
import dotenv
import sys
import tkinter as tk
import urllib.request

# Local imports
import SentralTimetable


class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        """Set the current selection"""
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        """Move the selection"""
        a = self.nearest(event.y)
        if a < self.curIndex:
            x = self.get(a)
            self.delete(a)
            self.insert(a + 1, x)
            self.curIndex = a
        elif a > self.curIndex:
            x = self.get(a)
            self.delete(a)
            self.insert(a - 1, x)
            self.curIndex = a


class App:
    """Overall class to manage the app."""

    def __init__(self):
        """Initialize the app."""
        self.frm_button = None
        self.btn_timetable = None
        self.btn_notices = None
        self.btn_events = None
        self.btn_me = None
        self.btn_settings = None
        self.btn_reload = None

        self.reload_manual = partial(self.reload, True)
        self.reload_auto = partial(self.reload, False)
        self.reload_manual.__name__ = "reload_manual"  # Stops AttributeError
        self.reload_auto.__name__ = "reload_auto"
        
        self.window = tk.Tk()
        self.window.title("Sentral")
        self.window.geometry("500x500")
        urllib.request.urlretrieve(
            "https://github.com/J-J-B-J/get-sentral/raw/main/docs/img/icon"
            ".png", "icon.png")
        self.window.iconphoto(
            True,
            tk.PhotoImage(file='icon.png')
        )
        self.window.bind("<Command-r>", self.reload_manual)

        self.notice_range_start = 0
        self.event_range_start = -1

        # Read the app data file to get the details
        details = dict(dotenv.dotenv_values("App_Credentials.env"))
        self.username = details.get("USERNAME", "")
        self.password = details.get("PASSWORD", "")
        self.url = details.get("URL", "")
        try:
            self.delay_reload = float(details.get("DELAY_RELOAD", 5.0))
        except ValueError:
            self.delay_reload = 5.0
        self.tabs = tuple(
            details.get("TABS", "Timetable,Notices,Events,Me").split(",")
        )
        self.start_tab = details.get("START_TAB", "Timetable")

        self.create_buttons()
        self.section_objects = []
        self.data = SentralTimetable.Sentral(
            [],
            [],
            [],
            SentralTimetable.User("", "", 0, "", "")
        )
        if self.start_tab == "Timetable":
            self.mode = self.timetable
        elif self.start_tab == "Notices":
            self.mode = self.notices
        elif self.start_tab == "Events":
            self.mode = self.events
        elif self.start_tab == "Me":
            self.mode = self.me
        else:
            self.mode = self.timetable

        self.window.after(int(self.delay_reload * 60000), self.reload_auto)

        self.last_reload = "N/A"

        if not self.username or not self.password or not self.url:
            self.settings()
        else:
            self.reload(manual=True)

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

        for tab in self.tabs:
            if tab == "Timetable":
                self.btn_timetable = create_button(
                    "Timetable", self.timetable
                )
            elif tab == "Notices":
                self.btn_notices = create_button(
                    "Notices", self.notices
                )
            elif tab == "Events":
                self.btn_events = create_button(
                    "Events", self.events
                )
            elif tab == "Me":
                self.btn_me = create_button(
                    "Me", self.me
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
        self.btn_reload.bind("<Button-1>", self.reload_manual)

    def destroy_section_objects(self):
        """Destroy all the objects in the section_objects list."""
        for object_ in self.section_objects:
            object_.destroy()
        self.section_objects = []

    def create_title_and_set_mode(self, title: str, mode: callable):
        """Create a title for the page."""
        lbl_title = tk.Label(
            self.window,
            text=title,
            font=("Arial", 20)
        )
        self.section_objects.append(lbl_title)
        lbl_title.pack(side=tk.TOP)
        self.mode = mode
        return lbl_title

    def reload(self, manual: bool = False, *_):
        """
        Reload the data in the background.
        :param manual: Whether the reload was activated by the user.
        """
        self.window.unbind("<Command-r>")
        self.btn_reload.config(state=tk.DISABLED)

        self.last_reload = datetime.datetime.now().strftime("%H:%M:%S")

        # Create a thread to reload the data
        def sentral(*_):
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

        reload_window = None

        if manual:  # Create the reload window
            # A list of the image objects for the reloading window
            images = [
                ImageTk.PhotoImage(
                    Image.open(f"./img/Loading/Sentral-{x}.png")
                ) for x in range(125)
            ]
            frame_num = 0

            reload_window = tk.Toplevel()
            reload_window.geometry("100x100")
            reload_window.resizable(False, False)
            reload_window.title("↻")

            frm_img = tk.Frame(reload_window, width=600, height=400)
            frm_img.pack()
            frm_img.place(anchor='center', relx=0.5, rely=0.5)

            # Create a Label Widget to display the text or Image
            lbl_img = tk.Label(frm_img, image=images[0])
            lbl_img.pack()

            def next_frame():
                """Go to the next frame in the animation"""
                nonlocal frame_num
                reload_window.after(15, next_frame)
                frame_num += 1
                if frame_num >= len(images):
                    frame_num = 0
                lbl_img.config(image=images[frame_num])
                reload_window.update()

            next_frame()

        # Reload the data
        def reload(*_):
            """To be run after the thread is finished."""
            if not sentral_thread.is_alive():
                self.window.bind("<Command-r>", self.reload_manual)
                self.btn_reload.config(state=tk.NORMAL)
                if manual:
                    reload_window.destroy()
                if self.mode == self.settings:
                    return
                elif self.mode == self.reload:
                    return
                else:
                    self.mode()
                self.window.after(int(self.delay_reload * 60000), self.reload)
            else:
                self.window.after(200, reload)

        reload()
    
    def create_increase_decrease(self, frame: tk.Frame, counter, 
                                 increment: int, data: list, increase_range,
                                 decrease_range):
        """
        Create the increase and decrease buttons for a page.
        :param frame: The frame in which to pack the buttons
        :param counter: The variable which keeps track of the count
        :param increment: The amount to increment the counter by
        :param data: The list of data that is being displayed
        :param increase_range: The callback for when the increase button is
        pressed
        :param decrease_range: The callback for when the decrease button is
        pressed
        """
        btn_increase_range = tk.Button(
            frame,
            text=">",
            width=10
        )
        self.section_objects.append(btn_increase_range)
        btn_increase_range.pack(side=tk.RIGHT)
        if counter + increment < len(data):
            btn_increase_range.bind("<Button-1>", increase_range)
        else:
            btn_increase_range.config(state=tk.DISABLED)

        btn_decrease_range = tk.Button(
            frame,
            text="<",
            width=10
        )
        self.section_objects.append(btn_decrease_range)
        btn_decrease_range.pack(side=tk.LEFT)
        if counter > 0:
            btn_decrease_range.bind("<Button-1>", decrease_range)
        else:
            btn_decrease_range.config(state=tk.DISABLED)

    def timetable(self, *_):
        """The 'timetable' page"""
        self.destroy_section_objects()
        self.create_title_and_set_mode("Timetable", self.timetable)

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

    def notices(self, *_):
        """The 'notices' page"""
        self.destroy_section_objects()
        self.create_title_and_set_mode("Notices", self.notices)

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

        def increase_range(*_):
            """Increase the range of notices shown"""
            self.notice_range_start += 5
            self.notices()

        def decrease_range(*_):
            """Decrease the range of notices shown"""
            self.notice_range_start -= 5
            self.notices()

        def open_notice(this_notice: SentralTimetable.Notice, *_):
            """Show the detail view for a notice"""
            notice_window = tk.Tk()
            notice_window.title('Notice')
            notice_window.geometry('500x150')
            notice_window.focus_set()
            notice_window.bind(
                "<Escape>",
                lambda _: notice_window.destroy()
            )

            lbl_title = tk.Label(
                notice_window,
                text=this_notice.title,
                font=("Arial", 20)
            )
            lbl_title.pack(side=tk.TOP)

            lbl_date = tk.Label(
                notice_window,
                text=f"By {this_notice.teacher} on "
                     f"{this_notice.date.day}/{this_notice.date.month}/"
                     f"{this_notice.date.year} at {this_notice.date.hour}:"
                     f"{this_notice.date.minute}"
            )
            lbl_date.pack(side=tk.TOP)

            lbl_content = tk.Label(
                notice_window,
                text=this_notice.content,
                wraplength=490
            )
            lbl_content.pack(side=tk.TOP)

            notice_window.mainloop()

        for notice in self.data.notices[
                      self.notice_range_start:self.notice_range_start + 5]:
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
        
        self.create_increase_decrease(frm_notices, self.notice_range_start, 5,
                                      self.data.notices, increase_range,
                                      decrease_range)

    def events(self, *_):
        """The 'timetable' page"""
        self.destroy_section_objects()
        self.create_title_and_set_mode("Events", self.events)

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

        def increase_range(*_):
            """Increase the range of events shown"""
            self.event_range_start += 1
            self.events()

        def decrease_range(*_):
            """Decrease the range of events shown"""
            self.event_range_start -= 1
            self.events()

        def open_event(event: SentralTimetable.Event, *_):
            """Show the detail view for an event"""
            event_window = tk.Tk()
            event_window.title('Event')
            event_window.geometry('500x150')
            event_window.focus_set()
            event_window.bind(
                "<Escape>",
                lambda _: event_window.destroy()
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

        def open_day(this_day: datetime.date, *_):
            """Show the events for a day"""
            day_window = tk.Tk()
            day_window.title(this_day.strftime("%A %d %B %Y"))
            day_window.geometry('500x150')
            day_window.focus_set()
            day_window.bind(
                "<Escape>",
                lambda _: day_window.destroy()
            )

            lbl_title = tk.Label(
                day_window,
                text=f"Events on "
                     f"{this_day.day}/{this_day.month}/{this_day.year}",
                font=("Arial", 20)
            )
            lbl_title.pack(side=tk.TOP)

            for event in self.data.events:
                if (event.date.dy, event.date.mth, event.date.yr) == \
                        (this_day.day, this_day.month, this_day.year):
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
        
        self.create_increase_decrease(frm_calendar, self.event_range_start, 1,
                                      months, increase_range, decrease_range)

    def me(self, *_):
        """The 'me' page"""
        self.destroy_section_objects()
        self.create_title_and_set_mode("Me", self.me)

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

        def show_barcode(*_):
            """Show the barcode in a new window"""
            barcode_window = tk.Tk()
            barcode_window.title("Barcode")
            barcode_window.geometry('593x90')
            barcode_window.focus_set()
            barcode_window.bind(
                "<Escape>",
                lambda _: barcode_window.destroy()
            )

            lbl_barcode = tk.Label(
                barcode_window,
                text=self.data.user.barcode,
                font=("Arial", 8)
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

        lbl_journal = tk.Label(
            frm_me,
            text="Journal",
            anchor=tk.W
        )
        self.section_objects.append(lbl_journal)
        lbl_journal.pack(side=tk.TOP, fill=tk.X)

        txt_journal = tk.Text(
            frm_me,
            width=50,
            height=10
        )
        self.section_objects.append(txt_journal)
        txt_journal.pack(side=tk.TOP)
        txt_journal.insert("1.0", self.data.user.journal)

        btn_save = tk.Button(
            frm_me,
            text="Save",
            width=10
        )
        self.section_objects.append(btn_save)
        btn_save.pack(side=tk.TOP)

        def save_journal(*_):
            """Save the journal in the background"""
            btn_save.config(text="Saving...", state=tk.DISABLED)
            txt_journal.config(state=tk.DISABLED)

            def save():
                """Save the journal"""
                journal = txt_journal.get("1.0", tk.END)
                self.data.user.journal = journal
                SentralTimetable.set_journal(
                    journal,
                    debug=False,
                    timeout=30,
                    usr=self.username,
                    pwd=self.password,
                    url=self.url
                )
                try:  # In case the elements have been destroyed
                    btn_save.config(text="Save", state=tk.NORMAL)
                    txt_journal.config(state=tk.NORMAL)
                    showinfo(message="Journal saved")
                except tk.TclError:
                    pass

            save_thread = Thread(target=save)
            save_thread.start()

        btn_save.bind("<Button-1>", save_journal)

    def settings(self, *_):
        """The 'settings' page"""
        self.destroy_section_objects()
        self.create_title_and_set_mode("Settings", self.settings)

        frm_settings = tk.Frame(self.window, width=500, height=500)
        self.section_objects.append(frm_settings)
        frm_settings.pack()

        def create_setting(name: str, help_text: str):
            """Create a setting label"""
            def show_help_window(title: str, text: str, *_):
                """Show a window with help text"""
                window = tk.Tk()
                window.title(title)
                window.geometry('250x100')
                window.resizable(False, True)
                window.focus_set()
                window.bind(
                    "<Escape>",
                    lambda _: window.destroy()
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
            return frm_setting

        def create_setting_entry(name: str, initial_text: str, frm_setting):
            """
            Create a setting's entry widget
            :param frm_setting: The frame for the setting
            :param name: The name of the setting
            :param initial_text: The initial text to put in the entry
            :return: The entry
            """
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

        def create_label(text: str):
            """Create a label"""
            lbl = tk.Label(
                frm_settings,
                text=text,
                fg="grey50"
            )
            self.section_objects.append(lbl)
            lbl.pack(side=tk.TOP, fill=tk.X)

        def create_text(text: str):
            """Create a label"""
            lbl = tk.Label(
                frm_settings,
                text=text
            )
            self.section_objects.append(lbl)
            lbl.pack(side=tk.TOP, fill=tk.X)

        # Create the User details
        create_label("Login details")
        frm_username = create_setting(
            "Username",
            "The username you use to login to Sentral"
        )
        ent_username = create_setting_entry(
            "Username",
            self.username,
            frm_username
        )
        frm_password = create_setting(
            "Password",
            "The password you use to login to Sentral"
        )
        ent_password = create_setting_entry(
            "Password",
            self.password,
            frm_password
        )
        frm_url = create_setting(
            "URL",
            "The URL of your school's Sentral dashboard. Must start with "
            "https:// and end with /portal/dashboard.\nE.g. "
            "https://examplehs.sentral.com.au/portal/dashboard"
        )
        ent_url = create_setting_entry(
            "URL",
            self.url,
            frm_url
        )

        # Create reload settings
        create_label("Reload")
        frm_delay_reload = create_setting(
            "Reload wait",
            "The number of minutes to wait before reloading the page. "
            "Must be a positive number."
        )
        ent_delay_reload = create_setting_entry(
            "Reload wait",
            str(self.delay_reload),
            frm_delay_reload
        )

        create_text(f"Last reloaded at {self.last_reload}")

        # Create the tab settings
        create_label("Tabs")
        frm_tab_order = create_setting(
            "Tab order",
            "The order of the tabs at the top of the app. "
            "Drag and drop to move."
        )
        ddlb_tabs = DragDropListbox(
            frm_tab_order,
            width=30,
            height=4  # The number of tabs, minus one
        )
        self.section_objects.append(ddlb_tabs)
        ddlb_tabs.pack(side=tk.RIGHT)

        for tab in self.tabs:
            ddlb_tabs.insert(tk.END, tab)

        frm_start_tab = create_setting(
            "Start tab",
            "The tab to open when the app is started"
        )
        var_start_tab = tk.StringVar()
        var_start_tab.set(self.start_tab)
        mnu_start_tab = tk.OptionMenu(
            frm_start_tab,
            var_start_tab,
            "Timetable", "Notices", "Events", "Me"
        )
        self.section_objects.append(mnu_start_tab)
        mnu_start_tab.pack(side=tk.RIGHT)
        mnu_start_tab.config(width=27)

        def save_settings(*_):
            """Save the settings"""

            def check_decimal(num: str):
                """Check if a number is a decimal number (or int)"""
                try:
                    float(num)
                    return True
                except ValueError:
                    return False

            self.username = ent_username.get()
            self.password = ent_password.get()
            self.url = ent_url.get()
            if check_decimal(ent_delay_reload.get()) and \
                    float(ent_delay_reload.get()) > 0:
                self.delay_reload = float(ent_delay_reload.get())
            else:
                showerror("Error", "Reload wait must be a positive number")
                return
            old_tabs = self.tabs
            self.tabs = ddlb_tabs.get(0, tk.END)
            # Save the data to the app data file
            dotenv.set_key("App_Credentials.env", "USERNAME", self.username)
            dotenv.set_key("App_Credentials.env", "PASSWORD", self.password)
            dotenv.set_key("App_Credentials.env", "URL", self.url)
            dotenv.set_key("App_Credentials.env", "DELAY_RELOAD",
                           str(self.delay_reload))
            dotenv.set_key("App_Credentials.env", "TABS", ','.join(self.tabs))
            dotenv.set_key("App_Credentials.env", "START_TAB",
                           var_start_tab.get())

            if askyesno("Saved", "Save complete. Do you want to reload?"):
                self.reload(manual=True)
            if old_tabs != self.tabs:
                self.destroy_section_objects()
                self.frm_button.destroy()
                self.create_buttons()
                self.settings()

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
        self.mode()
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
