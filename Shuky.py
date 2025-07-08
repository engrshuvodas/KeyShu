import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import time
import random
import webbrowser

# Global variables for timer and stop control
stop_flag = False
start_time = 0
timer_running = False

def open_portfolio():
    webbrowser.open_new("https://engrshuvodas.github.io/SHUVO-_portfolio/")

def show_about():
    messagebox.showinfo(
        "About KeyShu",
        "KeyShu - Human-Like Typing Bot\n"
        "Version: 1.0\n"
        "Created by: Engr Shuvo Das\n"
        "Created on: July 8, 2025\n\n"
        "This bot mimics human typing behavior with smart delays and randomness "
        "to avoid detection."
    )

def start_typing():
    text = input_text.get("1.0", tk.END).rstrip()
    try:
        delay = speed_slider.get() / 1000
    except:
        delay = 0.05

    if not text.strip():
        messagebox.showwarning("Empty Text", "Please enter some text to type.")
        return

    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    threading.Thread(target=type_text, args=(text, delay)).start()
    start_timer()

def type_text(text, delay):
    global stop_flag
    stop_flag = False
    lines = text.splitlines()
    time.sleep(5)  # Buffer to switch to typing field

    every_n = 10
    before_min, before_max = 4, 8
    after_min, after_max = 10, 20

    line_count = 0

    for line in lines:
        if stop_flag:
            break

        time.sleep(random.uniform(before_min, before_max))  # Delay before each line

        for char in line:
            if stop_flag:
                break
            pyautogui.write(char)
            time.sleep(random.uniform(0.05, 0.13))  # Per character delay

            if char in [".", ",", ";"]:
                time.sleep(random.uniform(0.2, 0.5))  # Extra pause on punctuation

        pyautogui.press("enter")
        line_count += 1

        if line_count % every_n == 0:
            time.sleep(random.uniform(after_min, after_max))  # Longer pause

    stop_timer()
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

def stop_typing():
    global stop_flag
    stop_flag = True
    stop_timer()
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

# Timer Functions
def start_timer():
    global timer_running, start_time
    timer_running = True
    start_time = time.time()
    threading.Thread(target=update_timer, daemon=True).start()

def stop_timer():
    global timer_running
    timer_running = False
    timer_label.config(text="Typing Time: 0 sec")

def update_timer():
    while timer_running:
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"Typing Time: {elapsed} sec")
        time.sleep(1)

# GUI setup
root = tk.Tk()
root.title("KeyShu - Human Typing Simulator")
root.geometry("620x540")
root.resizable(False, False)

# App Title
tk.Label(root, text="KeyShu - Human-Like Typing Bot", font=("Arial", 14, "bold"), fg="#0F7A6C").pack(pady=10)

# Text Area
tk.Label(root, text="Paste your text/code below:", font=("Arial", 12)).pack()
input_text = tk.Text(root, wrap=tk.WORD, height=10, font=("Consolas", 12))
input_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Speed Slider
tk.Label(root, text="Typing Speed (ms per character):", font=("Arial", 11)).pack(pady=(10, 0))
speed_slider = tk.Scale(root, from_=10, to=300, orient=tk.HORIZONTAL)
speed_slider.set(50)
speed_slider.pack()

# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

start_btn = tk.Button(frame, text="Start Typing (after 5s)", command=start_typing, bg="green", fg="white", font=("Arial", 11))
start_btn.pack(side=tk.LEFT, padx=10)

stop_btn = tk.Button(frame, text="Stop Typing", command=stop_typing, bg="red", fg="white", font=("Arial", 11), state="disabled")
stop_btn.pack(side=tk.LEFT, padx=10)

# Timer Display
timer_label = tk.Label(root, text="Typing Time: 0 sec", font=("Arial", 11), fg="blue")
timer_label.pack(pady=5)

# Note
tk.Label(root, text="Click the field where typing should happen within 5 seconds after starting.", fg="gray", font=("Arial", 9)).pack(pady=5)

# Footer Buttons
footer_frame = tk.Frame(root)
footer_frame.pack(pady=10)

about_btn = tk.Button(footer_frame, text="About", command=show_about, font=("Arial", 9))
about_btn.pack(side=tk.LEFT, padx=5)

credit_btn = tk.Button(footer_frame, text="Developed by Shuvo Das", font=("Arial", 9, "underline"), fg="blue", bd=0, cursor="hand2", command=open_portfolio)
credit_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
