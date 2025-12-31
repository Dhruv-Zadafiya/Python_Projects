from tkinter import *
from tkinter import ttk, messagebox
import calendar
import datetime

HOLIDAYS = [
    (1, 1, "Happy New Year"),
    (1, 14, "Makar Sankranti / Pongal"),
    (1, 26, "Republic Day"),
    (3,10, "Holi"),
    (8, 15, "Independence Day"),
    (12, 25, "Christmas"),
    
]

today = datetime.date.today()

def showCal(event=None):
    year_text = year_field.get()

    if not year_text.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid year.")
        return

    year = int(year_text)
    if year < 1800 or year > 9999:
        messagebox.showerror("Invalid Year", "Enter year between 1800–9999.")
        return

    win = Toplevel(root)
    win.title(f"Calendar - {year}")
    win.geometry("720x750")
    win.config(bg="#0F172A")

    ttk.Label(
        win,
        text=f"📅 Calendar - {year}",
        font=("Segoe UI", 20, "bold"),
        foreground="#38BDF8",
        background="#0F172A"
    ).pack(pady=15)

    frame = Frame(win, bg="#0F172A")
    frame.pack(fill=BOTH, expand=True, padx=15, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    text = Text(
        frame,
        font=("Consolas", 13),
        bg="#020617",
        fg="#E5E7EB",
        insertbackground="white",
        yscrollcommand=scrollbar.set,
        padx=10,
        pady=10
    )
    text.pack(fill=BOTH, expand=True)
    scrollbar.config(command=text.yview)

    text.tag_config("month", foreground="#38BDF8", font=("Consolas", 14, "bold"))
    text.tag_config("holiday", foreground="#F87171", font=("Consolas", 12, "bold"))
    text.tag_config("today", background="#22C55E", foreground="black", font=("Consolas", 12, "bold"))

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        text.insert(END, f"\n{month_name} {year}\n", "month")
        text.insert(END, calendar.month(year, month) + "\n")

        for m, d, name in HOLIDAYS:
            if m == month:
                pos = text.search(f"{d:2d}", "1.0", END)
                while pos:
                    text.tag_add("holiday", pos, f"{pos}+2c")
                    pos = text.search(f"{d:2d}", f"{pos}+2c", END)

        if year == today.year and month == today.month:
            pos = text.search(f"{today.day:2d}", "1.0", END)
            if pos:
                text.tag_add("today", pos, f"{pos}+2c")

    text.config(state=DISABLED)

def on_enter(e):
    e.widget.config(style="Hover.TButton")

def on_leave(e):
    e.widget.config(style="TButton")

root = Tk()
root.title("Calendar Application")
root.geometry("520x380")
root.config(bg="#0F172A")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 11, "bold"),
    padding=8,
    background="#1E293B",
    foreground="white"
)

style.configure(
    "Hover.TButton",
    background="#38BDF8",
    foreground="#020617"
)

ttk.Label(
    root,
    text="📆 Calendar Application",
    font=("Segoe UI", 22, "bold"),
    foreground="#38BDF8",
    background="#0F172A"
).pack(pady=25)

input_frame = Frame(root, bg="#0F172A")
input_frame.pack(pady=10)

ttk.Label(
    input_frame,
    text="Enter Year:",
    font=("Segoe UI", 12),
    foreground="white",
    background="#0F172A"
).grid(row=0, column=0, padx=10)

year_field = ttk.Entry(input_frame, width=18, font=("Segoe UI", 12))
year_field.grid(row=0, column=1, padx=10)
year_field.bind("<Return>", showCal)

btn_frame = Frame(root, bg="#0F172A")
btn_frame.pack(pady=30)

show_btn = ttk.Button(btn_frame, text="Show Calendar", command=showCal)
show_btn.grid(row=0, column=0, padx=12)
show_btn.bind("<Enter>", on_enter)
show_btn.bind("<Leave>", on_leave)

clear_btn = ttk.Button(btn_frame, text="Clear", command=lambda: year_field.delete(0, END))
clear_btn.grid(row=0, column=1, padx=12)
clear_btn.bind("<Enter>", on_enter)
clear_btn.bind("<Leave>", on_leave)

exit_btn = ttk.Button(btn_frame, text="Exit", command=root.destroy)
exit_btn.grid(row=0, column=2, padx=12)
exit_btn.bind("<Enter>", on_enter)
exit_btn.bind("<Leave>", on_leave)

root.mainloop()
