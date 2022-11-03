"""The app for get-sentral."""
import tkinter as tk
from threading import Thread
import SentralTimetable


class App:
    """Overall class to manage the app."""

    def __init__(self):
        """Initialize the app."""
        self.window = tk.Tk()
        self.window.title("Sentral")
        self.window.geometry("500x500")
        self.window.iconphoto(True, tk.PhotoImage(file='docs/img/icon.png'))
        self.create_buttons()
        self.section_objects = []
        self.data = SentralTimetable.Sentral(
            [],
            [],
            [],
            SentralTimetable.User("", "", 0, "")
        )

        self.state = 1
        self.reload()

    def create_buttons(self):
        """Create the buttons for the top of the app"""
        self.frm_button = tk.Frame(self.window, width=500)
        self.frm_button.pack()

        self.btn_timetable = tk.Button(
            self.frm_button,
            text="Timetable",
            width=10
        )
        self.btn_timetable.pack(side=tk.LEFT)
        self.btn_notices = tk.Button(
            self.frm_button,
            text="Notices",
            width=10
        )
        self.btn_notices.pack(side=tk.LEFT)
        self.btn_events = tk.Button(
            self.frm_button,
            text="Events",
            width=10
        )
        self.btn_events.pack(side=tk.LEFT)
        self.btn_me = tk.Button(
            self.frm_button,
            text="Me",
            width=10
        )
        self.btn_me.pack(side=tk.LEFT)
        self.btn_settings = tk.Button(
            self.frm_button,
            text="Settings",
            width=10
        )
        self.btn_settings.pack(side=tk.LEFT)
        self.btn_reload = tk.Button(
            self.frm_button,
            text="↻",
            width=3
        )
        self.btn_reload.pack()

        self.btn_timetable.bind("<Button-1>", self.timetable)
        self.btn_notices.bind("<Button-1>", self.notices)
        self.btn_events.bind("<Button-1>", self.events)
        self.btn_me.bind("<Button-1>", self.me)
        self.btn_settings.bind("<Button-1>", self.settings)
        self.btn_reload.bind("<Button-1>", self.reload)

    def reload(self, *args):
        """Reload the data"""
        self.btn_reload.config(state=tk.DISABLED)
        self.btn_reload.unbind("<Button-1>")

        reload_window = tk.Tk()
        reload_window.title('↻')
        reload_window.geometry('100x25')
        reload_window.resizable(False, False)
        lbl_reload = tk.Label(reload_window, text='Reloading.')
        lbl_reload.pack(side=tk.LEFT)

        def sentral(*args):
            """Get the timetable"""
            self.data = SentralTimetable.get_timetable()

        sentral_thread = Thread(target=sentral)
        sentral_thread.start()

        def reload(*args):
            """Reload the 'reload' window"""
            if self.state == 5:
                lbl_reload.config(text='Reloading.')
                self.state = 1
            else:
                lbl_reload.config(text=lbl_reload['text'] + '.')
                self.state += 1
            if not sentral_thread.is_alive():
                reload_window.destroy()
                self.btn_reload.config(state=tk.NORMAL)
                self.btn_reload.bind("<Button-1>", self.reload)
            else:
                reload_window.after(200, reload)

        reload()
        self.window.focus_set()

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

    def timetable(self, *args):
        """The 'timetable' page"""
        self.destroy_section_objects()

        lbl_title = self.create_title("Timetable")

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

        lbl_title = self.create_title("Notices")

    def events(self, *args):
        """The 'timetable' page"""
        self.destroy_section_objects()

        lbl_title = self.create_title("Events")

    def me(self, *args):
        """The 'me' page"""
        self.destroy_section_objects()

        lbl_title = self.create_title("Me")

    def settings(self, *args):
        """The 'settings' page"""
        self.destroy_section_objects()

        lbl_title = self.create_title("Settings")

    def run(self):
        """Run the app."""
        self.timetable()
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
