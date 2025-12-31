# Welcome to simple clock using Python.....
from tkinter import *
import datetime

is_24h = False
blink = True
is_fullscreen = False

def set_12h():
    global is_24h
    is_24h = False
    lab_am.config(text="AM", fg="#FF4081")

def set_24h():
    global is_24h
    is_24h = True
    lab_am.config(text="", fg="gray")

def set_dark():
    apply_theme(dark=True)

def set_light():
    apply_theme(dark=False)

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    clock.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = False
    clock.attributes("-fullscreen", False)

def apply_theme(dark=True):
    if dark:
        bg = "#272736"
        box = "#3B3F5C"
        fg = "white"
        btn_bg = "#3B3F5C"
    else:
        bg = "#F4F6FB"
        box = "#FFFFFF"
        fg = "black"
        btn_bg = "#E0E0E0"

    clock.config(bg=bg)
    btn_frame.config(bg=bg)

    for w in labels:
        w.config(bg=box, fg=fg)

    for b in (btn_12, btn_24, btn_dark, btn_light):
        b.config(bg=btn_bg, fg=fg)
        b.default_bg = btn_bg
        b.default_fg = fg

def date_time():
    global blink
    now = datetime.datetime.now()

    hr = now.strftime('%H' if is_24h else '%I')
    mi = now.strftime('%M')
    sec = now.strftime('%S')
    am = now.strftime('%p')
    day = now.strftime('%a')
    date = now.strftime('%d %b %Y')

    sep = ":" if blink else " "
    blink = not blink

    lab_time.config(text=f"{hr}{sep}{mi}{sep}{sec}")

    if not is_24h:
        lab_am.config(text=am)

    lab_date.config(text=f"{day}, {date}")
    clock.after(1000, date_time)


def on_enter(btn):
    btn.config(bg="#5C7CFA", fg="white")

def on_leave(btn):
    btn.config(bg=btn.default_bg, fg=btn.default_fg)

clock = Tk()
clock.title("Smart Digital Clock")
clock.geometry("900x400")
clock.resizable(True, True)

clock.bind("<F11>", toggle_fullscreen)
clock.bind("<Escape>", exit_fullscreen)

lab_time = Label(clock, font=('Segoe UI', 60, 'bold'))
lab_time.pack(pady=25)

lab_am = Label(clock, font=('Segoe UI', 28, 'bold'), width=6)
lab_am.pack()

lab_date = Label(clock, font=('Segoe UI', 18))
lab_date.pack(pady=8)

btn_frame = Frame(clock)
btn_frame.pack(pady=15)

btn_12 = Button(btn_frame, text="12 Hour", command=set_12h,
                font=('Segoe UI', 12), width=10,
                relief="flat", cursor="hand2")
btn_12.grid(row=0, column=0, padx=6)

btn_24 = Button(btn_frame, text="24 Hour", command=set_24h,
                font=('Segoe UI', 12), width=10,
                relief="flat", cursor="hand2")
btn_24.grid(row=0, column=1, padx=6)

btn_dark = Button(btn_frame, text="Dark Mode", command=set_dark,
                  font=('Segoe UI', 12), width=10,
                  relief="flat", cursor="hand2")
btn_dark.grid(row=0, column=2, padx=6)

btn_light = Button(btn_frame, text="Light Mode", command=set_light,
                   font=('Segoe UI', 12), width=10,
                   relief="flat", cursor="hand2")
btn_light.grid(row=0, column=3, padx=6)

labels = [lab_time, lab_am, lab_date]

for btn in (btn_12, btn_24, btn_dark, btn_light):
    btn.bind("<Enter>", lambda e, b=btn: on_enter(b))
    btn.bind("<Leave>", lambda e, b=btn: on_leave(b))

apply_theme(dark=True)
set_12h()
date_time()

clock.mainloop()
