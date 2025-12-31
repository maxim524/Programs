import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar
import winsound

root = tk.Tk()
root.title("Countdown")
root.geometry("460x520")
root.resizable(False, False)

paused = False
fullscreen = False
target_time = None
dark_mode = True

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#121212" if dark_mode else "white"
    fg = "white" if dark_mode else "black"
    dark_btn.config(text="🌑 Dark mode" if dark_mode else "🌞 Light mode")
    root.configure(bg=bg)
    for w in root.winfo_children():
        try:
            w.configure(background=bg, foreground=fg)
        except:
            pass

def easter_sunday(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return month, day

def play_melody():
    notes = [
        (523, 300),(587, 300),(698, 300),(784, 400),(659, 300),
        (587, 300),(523, 400),(523, 300),(587, 300),(698, 300),
        (659, 300),(587, 300),(523, 400),(587, 300),(659, 300),
        (698, 300),(784, 400),(659, 300),(587, 300),(523, 300),
        (587, 300),(698, 300),(784, 400),(659, 300),(523, 400)
    ]
    for freq, dur in notes:
        winsound.Beep(freq, dur)

def apply_preset(event=None):
    now = datetime.now()
    y = now.year
    choice = preset_var.get()
    if choice == "🎄 Christmas":
        set_date(y, 12, 24, 0, 0, 0)
    elif choice == "🎆 New Year's Eve":
        set_date(y, 12, 31, 23, 59, 59)
    elif choice == "🎉 New Year":
        set_date(y + 1, 1, 1, 0, 0, 0)
    elif choice == "🐣 Easter":
        m, d = easter_sunday(y)
        set_date(y, m, d, 0, 0, 0)
    elif choice == "🧨 Test (10 sec)":
        t = now + timedelta(seconds=10)
        set_date(t.year, t.month, t.day, t.hour, t.minute, t.second)

def set_date(y, m, d, h, mi, s):
    year_var.set(y)
    month_var.set(m)
    update_days()
    day_var.set(d)
    hour_var.set(h)
    min_var.set(mi)
    sec_var.set(s)

def update_days(*args):
    y = int(year_var.get())
    m = int(month_var.get())
    max_days = calendar.monthrange(y, m)[1]
    day_box["values"] = list(range(1, max_days + 1))
    if int(day_var.get()) > max_days:
        day_var.set(max_days)

def start():
    global target_time, paused
    paused = False
    target_time = datetime(
        int(year_var.get()), int(month_var.get()), int(day_var.get()),
        int(hour_var.get()), int(min_var.get()), int(sec_var.get())
    )
    countdown()

def countdown():
    if paused or not target_time:
        return
    diff = target_time - datetime.now()
    if diff.total_seconds() <= 0:
        result_label.config(text="🎉 DONE")
        play_melody()
        return
    d = diff.days
    h, r = divmod(diff.seconds, 3600)
    m, s = divmod(r, 60)
    result_label.config(text=f"{d} days {h:02d}:{m:02d}:{s:02d}")
    root.after(1000, countdown)

def toggle_pause():
    global paused
    paused = not paused
    pause_btn.config(text="▶ Resume" if paused else "⏸ Pause")
    if not paused:
        countdown()

def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

now = datetime.now()
year_var = tk.StringVar(value=now.year)
month_var = tk.StringVar(value=now.month)
day_var = tk.StringVar(value=now.day)
hour_var = tk.StringVar(value=0)
min_var = tk.StringVar(value=0)
sec_var = tk.StringVar(value=0)
preset_var = tk.StringVar(value="— Select Holiday —")

ttk.Label(root, text="🎯 Presets").pack(pady=4)
preset_box = ttk.Combobox(
    root, textvariable=preset_var, state="readonly",
    values=["🎄 Christmas","🎆 New Year's Eve","🎉 New Year","🐣 Easter","🧨 Test (10 sec)"]
)
preset_box.pack()
preset_box.bind("<<ComboboxSelected>>", apply_preset)

ttk.Separator(root).pack(fill="x", pady=10)

ttk.Label(root, text="Year").pack()
ttk.Combobox(root, textvariable=year_var, values=list(range(2024, 2101)), state="readonly").pack()

ttk.Label(root, text="Month").pack()
ttk.Combobox(root, textvariable=month_var, values=list(range(1, 13)), state="readonly").pack()

ttk.Label(root, text="Day").pack()
day_box = ttk.Combobox(root, textvariable=day_var, state="readonly")
day_box.pack()

ttk.Label(root, text="Time (H:M:S)").pack(pady=5)
frame = tk.Frame(root)
frame.pack()
ttk.Combobox(frame, width=4, textvariable=hour_var, values=list(range(24)), state="readonly").pack(side="left")
ttk.Label(frame, text=" : ").pack(side="left")
ttk.Combobox(frame, width=4, textvariable=min_var, values=list(range(60)), state="readonly").pack(side="left")
ttk.Label(frame, text=" : ").pack(side="left")
ttk.Combobox(frame, width=4, textvariable=sec_var, values=list(range(60)), state="readonly").pack(side="left")

ttk.Button(root, text="▶ Start", command=start).pack(pady=6)
pause_btn = ttk.Button(root, text="⏸ Pause", command=toggle_pause)
pause_btn.pack()
ttk.Button(root, text="🖥 Fullscreen", command=toggle_fullscreen).pack(pady=6)
dark_btn = ttk.Button(root, text="🌑 Dark mode", command=toggle_dark_mode)
dark_btn.pack(pady=6)

result_label = ttk.Label(root, text="Waiting...", font=("Arial", 18))
result_label.pack(pady=15)

year_var.trace("w", update_days)
month_var.trace("w", update_days)
update_days()
root.configure(bg="#121212")
root.mainloop()
