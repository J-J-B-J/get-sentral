"""Set the contents of your daily journal"""
import tkinter as tk
from tkinter.messagebox import *
from SentralTimetable import set_journal, get_timetable


# Yes I could have just done this as a text-based thing but that would be bad
# so yeah I used tkinter instead


def main():
    """The main function"""
    window = tk.Tk()
    window.geometry("500x200")
    window.title("Set Journal")

    showinfo(message="Loading...")
    txt_journal = tk.Text(
        master=window,
        width=65,
        height=12,
        borderwidth=2,
        relief=tk.GROOVE
    )
    txt_journal.insert("1.0", get_timetable().user.journal)
    txt_journal.pack()

    def save(_):
        """Save the journal"""
        journal = txt_journal.get("1.0", tk.END)
        showinfo(message="Saving journal...")
        set_journal(journal)
        showinfo(message="Journal saved")


    btn_save = tk.Button(
        master=window,
        width=8,
        text="Save"
    )
    btn_save.bind("<Button-1>", save)
    btn_save.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
