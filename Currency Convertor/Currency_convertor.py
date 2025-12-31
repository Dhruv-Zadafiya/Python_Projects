#  Advanced Currency Converter (Modern UI)
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

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
            status_label.config(text="Status: Online", fg="#00ff9c")
            return response.json()
        elif response.status_code == 429:
            messagebox.showerror("API Limit", "API request limit reached")
    except:
        status_label.config(text="Status: Offline", fg="red")
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
        amount /= rates[from_code]

    result = amount * rates[to_code]
    result_label.config(text=f"{result:.2f} {to_code}")

    history_list.insert(
        tk.END,
        f"{datetime.now().strftime('%H:%M:%S')} | {from_code} → {to_code} = {result:.2f}"
    )


def hover(widget, on, off):
    widget.bind("<Enter>", lambda e: widget.config(bg=on))
    widget.bind("<Leave>", lambda e: widget.config(bg=off))


root = tk.Tk()
root.title("🌍 Advanced Currency Converter")
root.geometry("900x550")
root.resizable(True,True)
root.configure(bg="#0f172a")

tk.Label(
    root,
    text="🌍 Advanced Currency Converter",
    font=("Segoe UI", 22, "bold"),
    fg="#38bdf8",
    bg="#0f172a"
).pack(pady=15)

main = tk.Frame(root, bg="#0f172a")
main.pack(fill="both", expand=True, padx=20)

left = tk.Frame(main, bg="#111827", padx=20, pady=20)
left.pack(side="left", fill="y")

right = tk.Frame(main, bg="#111827", padx=20, pady=20)
right.pack(side="right", fill="both", expand=True)

currency_map = {}

label_style = {"fg": "#cbd5f5", "bg": "#111827", "font": ("Segoe UI", 10)}

tk.Label(left, text="Amount", **label_style).pack(anchor="w")
amount_entry = tk.Entry(left, font=("Segoe UI", 12), bg="#020617",
                        fg="white", insertbackground="white", relief="flat")
amount_entry.pack(fill="x", pady=5)

tk.Label(left, text="From Currency", **label_style).pack(anchor="w")
from_var = tk.StringVar()
from_menu = tk.OptionMenu(left, from_var, "")
from_menu.config(bg="#020617", fg="white", relief="flat")
from_menu.pack(fill="x", pady=5)

tk.Label(left, text="To Currency", **label_style).pack(anchor="w")
to_var = tk.StringVar()
to_menu = tk.OptionMenu(left, to_var, "")
to_menu.config(bg="#020617", fg="white", relief="flat")
to_menu.pack(fill="x", pady=5)

convert_btn = tk.Button(
    left, text="Convert", font=("Segoe UI", 11, "bold"),
    bg="#22c55e", fg="black", relief="flat", height=2,
    command=convert_currency
)
convert_btn.pack(fill="x", pady=10)
hover(convert_btn, "#4ade80", "#22c55e")

refresh_btn = tk.Button(
    left, text="Refresh Rates", font=("Segoe UI", 10),
    bg="#3b82f6", fg="white", relief="flat", height=2,
    command=load_currencies
)
refresh_btn.pack(fill="x")
hover(refresh_btn, "#60a5fa", "#3b82f6")

result_label = tk.Label(
    left, text="", font=("Segoe UI", 15, "bold"),
    fg="#22c55e", bg="#020617", pady=10
)
result_label.pack(fill="x", pady=15)

tk.Label(
    right, text="Conversion History",
    fg="#38bdf8", bg="#111827",
    font=("Segoe UI", 14, "bold")
).pack(anchor="w")

history_frame = tk.Frame(right, bg="#020617")
history_frame.pack(fill="both", expand=True, pady=10)

history_list = tk.Listbox(
    history_frame, bg="#020617", fg="white",
    selectbackground="#334155", relief="flat"
)
history_list.pack(fill="both", expand=True)

status_label = tk.Label(
    root, text="Status: Ready",
    bg="#020617", fg="white", anchor="w", padx=10
)
status_label.pack(side="bottom", fill="x")

load_currencies()
root.mainloop()
