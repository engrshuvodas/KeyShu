import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import time
import random
import webbrowser
from tkinter import font as tkfont

# Global variables for timer and stop control
stop_flag = False
start_time = 0
timer_running = False

def open_portfolio():
    webbrowser.open_new("https://engrshuvodas.github.io/SHUVO-_portfolio/")

def show_about():
    messagebox.showinfo(
        "About Shuky",
        "Shuky - Advanced Human-Like Typing Bot\n"
        "Version: 2.0\n"
        "Developed by: Engr Shuvo Das\n"
        "Created on: July 9, 2025\n\n"
        "Features:\n"
        "- Intelligent typing patterns with random delays\n"
        "- Punctuation-aware pauses\n"
        "- Line break randomization\n"
        "- Anti-detection algorithms\n"
        "- Customizable typing speed\n\n"
        "© 2025 Shuvo Das - All Rights Reserved"
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

    # Advanced typing patterns
    every_n = random.randint(8, 15)  # Randomize the line count for long pauses
    before_min, before_max = 2, 6    # Reduced initial delay
    after_min, after_max = 8, 15     # Reduced line delay
    
    # Error simulation parameters
    error_chance = 0.03  # 3% chance of making an error
    correction_delay = 0.3  # Delay when correcting errors
    
    line_count = 0

    for line in lines:
        if stop_flag:
            break

        time.sleep(random.uniform(before_min, before_max))  # Delay before each line

        for i, char in enumerate(line):
            if stop_flag:
                break
            
            # Simulate occasional errors
            if random.random() < error_chance and i > 3:
                # Type wrong character
                wrong_char = chr(ord(char) + random.randint(-2, 2))
                pyautogui.write(wrong_char)
                time.sleep(correction_delay)
                # Backspace and correct
                pyautogui.press('backspace')
                time.sleep(correction_delay/2)
                pyautogui.write(char)
            else:
                pyautogui.write(char)
            
            # Variable typing speed with more randomness
            time.sleep(random.uniform(delay*0.7, delay*1.5))
            
            # Special delays for punctuation
            if char in [".", "!", "?"]:
                time.sleep(random.uniform(0.3, 0.8))
            elif char in [",", ";", ":"]:
                time.sleep(random.uniform(0.2, 0.5))

        # Randomize line breaks
        if line_count < len(lines) - 1:  # Don't press enter after last line
            pyautogui.press("enter")
            line_count += 1

            # Variable pause between paragraphs
            if line.strip() == "":
                time.sleep(random.uniform(1.5, 3.5))
            elif line_count % every_n == 0:
                time.sleep(random.uniform(after_min, after_max))
            else:
                time.sleep(random.uniform(0.5, 1.5))

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
root.title("Shuky - Advanced Typing Assistant")
root.geometry("650x580")
root.resizable(False, False)

# Custom colors
bg_color = "#f0f8ff"
primary_color = "#2c3e50"
secondary_color = "#3498db"
accent_color = "#e74c3c"

# Set background
root.configure(bg=bg_color)

# Custom font
title_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
label_font = tkfont.Font(family="Arial", size=11)
button_font = tkfont.Font(family="Arial", size=10)

# App Logo and Title Frame
title_frame = tk.Frame(root, bg=bg_color)
title_frame.pack(pady=(10, 5))

# Logo (using text as logo)
logo_label = tk.Label(title_frame, text="✍️", font=("Arial", 24), bg=bg_color)
logo_label.pack(side=tk.LEFT, padx=5)

app_title = tk.Label(title_frame, text="Shuky Typing Assistant", font=title_font, fg=primary_color, bg=bg_color)
app_title.pack(side=tk.LEFT)

# Info button with icon
info_icon = tk.Label(title_frame, text="ℹ️", font=("Arial", 12), cursor="hand2", bg=bg_color)
info_icon.bind("<Button-1>", lambda e: show_about())
info_icon.pack(side=tk.RIGHT, padx=10)

# Text Area Frame
text_frame = tk.Frame(root, bg=bg_color)
text_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

tk.Label(text_frame, text="Enter or paste your text below:", font=label_font, bg=bg_color).pack(anchor="w")

input_text = tk.Text(text_frame, wrap=tk.WORD, height=12, font=("Consolas", 11), padx=10, pady=10,
                    borderwidth=2, relief="groove", undo=True)
input_text.pack(fill=tk.BOTH, expand=True)

# Speed Control Frame
speed_frame = tk.Frame(root, bg=bg_color)
speed_frame.pack(pady=(10, 5), padx=10, fill=tk.X)

tk.Label(speed_frame, text="Typing Speed (ms per character):", font=label_font, bg=bg_color).pack(anchor="w")

speed_slider = tk.Scale(speed_frame, from_=10, to=300, orient=tk.HORIZONTAL, 
                       bg=bg_color, highlightthickness=0, troughcolor="#d5d5d5",
                       activebackground=secondary_color)
speed_slider.set(50)
speed_slider.pack(fill=tk.X)

# Button Frame
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)

start_btn = tk.Button(button_frame, text="Start Typing (5s delay)", command=start_typing, 
                     bg=secondary_color, fg="white", font=button_font, padx=15,
                     activebackground="#2980b9", relief="raised", bd=2)
start_btn.pack(side=tk.LEFT, padx=10)

stop_btn = tk.Button(button_frame, text="Stop Typing", command=stop_typing, 
                    bg=accent_color, fg="white", font=button_font, padx=15,
                    activebackground="#c0392b", state="disabled", relief="raised", bd=2)
stop_btn.pack(side=tk.LEFT, padx=10)

# Timer Display
timer_frame = tk.Frame(root, bg=bg_color)
timer_frame.pack(pady=5)

timer_label = tk.Label(timer_frame, text="Typing Time: 0 sec", font=label_font, fg=primary_color, bg=bg_color)
timer_label.pack()

# Note Label
note_frame = tk.Frame(root, bg=bg_color)
note_frame.pack(pady=5)

tk.Label(note_frame, 
        text="Note: Click the target field within 5 seconds after starting. The bot includes random delays for human-like behavior.",
        fg="#7f8c8d", font=("Arial", 9), bg=bg_color, wraplength=500).pack()

# Footer Frame
footer_frame = tk.Frame(root, bg=bg_color)
footer_frame.pack(pady=(10, 5))

dev_btn = tk.Button(footer_frame, text="Developed by Shuvo Das", font=("Arial", 9, "underline"), 
                   fg=primary_color, bg=bg_color, bd=0, cursor="hand2", 
                   activebackground=bg_color, activeforeground=secondary_color,
                   command=open_portfolio)
dev_btn.pack()

root.mainloop()