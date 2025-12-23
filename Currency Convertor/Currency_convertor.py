import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from datetime import datetime
import os



# This is my first API based Currency Converter Project with GUI using Tkinter.
API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def get_flag(code):
    try:
        return chr(127397 + ord(code[0])) + chr(127397 + ord(code[1]))
    except:
        return "🌍"

def fetch_rates():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            status_label.config(text="Status: Online ", bg="#222", fg="lime")
            return response.json()
        elif response.status_code == 429:
            messagebox.showerror("API Limit", "API request limit reached")
    except:
        status_label.config(text="Status: Offline ", bg="#222", fg="red")
        messagebox.showerror("Network Error", "Internet not available")
    return None

def validate_amount():
    try:
        value = float(amount_entry.get())
        if value <= 0:
            raise ValueError
        return value
    except:
        messagebox.showerror("Invalid Input", "Enter a valid positive number")
        return None

def load_currencies():
    data = fetch_rates()
    if not data:
        return

    rates = data["rates"]
    currency_map.clear()
    from_menu["menu"].delete(0, "end")
    to_menu["menu"].delete(0, "end")

    for code in sorted(rates.keys()):
        display = f"{get_flag(code)}  {code}"
        currency_map[display] = code
        from_menu["menu"].add_command(
            label=display, command=lambda v=display: from_var.set(v))
        to_menu["menu"].add_command(
            label=display, command=lambda v=display: to_var.set(v))

    from_var.set("🇺🇸  USD")
    to_var.set("🇮🇳  INR")

def convert_currency():
    amount = validate_amount()
    if amount is None:
        return

    data = fetch_rates()
    if not data:
        return

    rates = data["rates"]
    from_code = currency_map[from_var.get()]
    to_code = currency_map[to_var.get()]

    if from_code != "USD":
        amount = amount / rates[from_code]

    result = amount * rates[to_code]
    result_label.config(text=f"{result:.2f} {to_code}")

    history_list.insert(
        tk.END,
        f"{datetime.now().strftime('%H:%M:%S')} | {from_code} → {to_code} = {result:.2f}"
    )

def hover(widget, color_on, color_off):
    widget.bind("<Enter>", lambda e: widget.config(bg=color_on))
    widget.bind("<Leave>", lambda e: widget.config(bg=color_off))

root = tk.Tk()
root.title("🌍 Advanced Currency Converter")
root.geometry("900x550")
root.resizable(False, False)

overlay = tk.Frame(root, bg="#399EB8")
overlay.place(relwidth=1, relheight=1)
overlay.attributes = None

tk.Label(
    overlay,
    text="🌍 Advanced Currency Converter",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#399EB8"
).pack(pady=15)

main = tk.Frame(overlay, bg="#399EB8")
main.pack(padx=20, pady=10, fill="both", expand=True)

left = tk.Frame(main, bg="#399EB8", padx=20)
left.pack(side="left", fill="y")

right = tk.Frame(main, bg="#399EB8", padx=20)
right.pack(side="right", fill="both", expand=True)

currency_map = {}

tk.Label(left, text="Amount", fg="white", bg="#399EB8").pack()
amount_entry = tk.Entry(left, width=20)
amount_entry.pack(pady=5)

tk.Label(left, text="From Currency", fg="white", bg="#399EB8").pack()
from_var = tk.StringVar()
from_menu = tk.OptionMenu(left, from_var, "")
from_menu.pack()

tk.Label(left, text="To Currency", fg="white", bg="#111").pack()
to_var = tk.StringVar()
to_menu = tk.OptionMenu(left, to_var, "")
to_menu.pack()

convert_btn = tk.Button(
    left, text="Convert", bg="#28a745", fg="white",
    font=("Arial", 11, "bold"), width=15, command=convert_currency
)
convert_btn.pack(pady=10)
hover(convert_btn, "#34d058", "#2AEA57")

refresh_btn = tk.Button(
    left, text="Refresh Rates", bg="#007bff", fg="white",
    width=15, command=load_currencies
)
refresh_btn.pack()
hover(refresh_btn, "#9047c8", "#9047c8")

result_label = tk.Label(left, text="", font=("Arial", 14, "bold"),
                        fg="black", bg="#F3F4F4", width=25)
result_label.pack(pady=15)

tk.Label(right, text="Conversion History",
         fg="white", bg="#399EB8", font=("Arial", 14, "bold")).pack()

history_list = tk.Listbox(
    right, height=18, width=55,
    bg="#399EB8", fg="white", selectbackground="#222", borderwidth=0
)
history_frame = tk.Frame(right, bg="#222", bd=2, relief="ridge")
history_frame.pack(pady=10, padx=5, fill="both", expand=True)

history_list = tk.Listbox(
    history_frame,
    height=18,
    width=55,
    bg="#399EB8",
    fg="white",
    selectbackground="#222",
    borderwidth=0,  
)
history_list.pack(fill="both", expand=True)

history_list.pack(pady=10)

status_label = tk.Label(
    root, text="Status: Ready",
    bg="#399EB8", fg="white", anchor="w"
)
status_label.pack(side="bottom", fill="x")

load_currencies()
root.mainloop()
