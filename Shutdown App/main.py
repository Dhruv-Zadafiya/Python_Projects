# This is Simple Power Control Application....
from tkinter import *
import os

def restart():
    os.system("shutdown /r /t 1")

def restart_time():
    os.system("shutdown /r /t 20")

def logout():
    os.system("shutdown -l")

def lockscreen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def shutdown():
    os.system("shutdown /s /t 1")

def on_enter(e):
    e.widget['background'] = '#00ADB5'
    e.widget['foreground'] = 'black'

def on_leave(e):
    e.widget['background'] = '#222831'
    e.widget['foreground'] = 'white'

st = Tk()
st.title("Power Control")
st.geometry("500x550")
st.config(bg="#000000")
st.resizable(True, True)

Label(
    st,
    text="⚡ Power Control",
    font=("Segoe UI", 26, "bold"),
    bg="#050505",
    fg="#00ADB5"
).pack(pady=25)

def create_button(text, cmd, y):
    btn = Button(
        st,
        text=text,
        font=("Segoe UI", 16, "bold"),
        bg="#5E8D86",
        fg="white",
        relief=FLAT,
        cursor="hand2",
        command=cmd
    )
    btn.place(x=125, y=y, width=250, height=50)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

create_button("🔄 Restart", restart, 110)
create_button("⏱ Restart After 20s", restart_time, 180)
create_button("🚪 Logout", logout, 250)
create_button("🔒 Lock Screen", lockscreen, 320)
create_button("⏻ Shutdown", shutdown, 390)

st.mainloop()
