import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import time
import random
import webbrowser
from tkinter import font as tkfont

# Global variables
stop_flag = False
start_time = 0
timer_running = False

# Default timing parameters (all values in milliseconds)
DEFAULT_PARAMS = {
    'char_delay_min': 50,
    'char_delay_max': 150,
    'punctuation_extra_min': 200,
    'punctuation_extra_max': 500,
    'line_delay_min': 2000,
    'line_delay_max': 6000,
    'long_pause_every': 8,
    'long_pause_min': 8000,
    'long_pause_max': 15000,
    'error_rate': 3,
    'error_correction_min': 300,
    'error_correction_max': 600,
    'initial_delay': 5000
}

def open_portfolio():
    webbrowser.open_new("https://engrshuvodas.github.io/SHUVO-_portfolio/")

def show_about():
    messagebox.showinfo(
        "About Shuky",
        "Shuky - Advanced Human-Like Typing Bot\n"
        "Version: 2.1\n"
        "Developed by: Engr Shuvo Das\n\n"
        "Advanced Features:\n"
        "- Fully customizable random timing for each character\n"
        "- Never repeats the same delay pattern\n"
        "- Error simulation with correction\n"
        "- Anti-detection algorithms\n\n"
        "© 2025 Shuvo Das - All Rights Reserved"
    )

class TimingControls:
    def __init__(self, parent):
        self.frame = tk.LabelFrame(parent, text="Timing Controls (milliseconds)", font=("Arial", 10), padx=5, pady=5)
        
        # Character Timing
        tk.Label(self.frame, text="Char Delay:").grid(row=0, column=0, sticky="e")
        self.char_min = tk.Entry(self.frame, width=5)
        self.char_min.insert(0, DEFAULT_PARAMS['char_delay_min'])
        self.char_min.grid(row=0, column=1)
        tk.Label(self.frame, text="to").grid(row=0, column=2)
        self.char_max = tk.Entry(self.frame, width=5)
        self.char_max.insert(0, DEFAULT_PARAMS['char_delay_max'])
        self.char_max.grid(row=0, column=3)
        
        # Punctuation Timing
        tk.Label(self.frame, text="Punctuation+:").grid(row=1, column=0, sticky="e")
        self.punct_min = tk.Entry(self.frame, width=5)
        self.punct_min.insert(0, DEFAULT_PARAMS['punctuation_extra_min'])
        self.punct_min.grid(row=1, column=1)
        tk.Label(self.frame, text="to").grid(row=1, column=2)
        self.punct_max = tk.Entry(self.frame, width=5)
        self.punct_max.insert(0, DEFAULT_PARAMS['punctuation_extra_max'])
        self.punct_max.grid(row=1, column=3)
        
        # Line Timing
        tk.Label(self.frame, text="Line Delay:").grid(row=2, column=0, sticky="e")
        self.line_min = tk.Entry(self.frame, width=5)
        self.line_min.insert(0, DEFAULT_PARAMS['line_delay_min'])
        self.line_min.grid(row=2, column=1)
        tk.Label(self.frame, text="to").grid(row=2, column=2)
        self.line_max = tk.Entry(self.frame, width=5)
        self.line_max.insert(0, DEFAULT_PARAMS['line_delay_max'])
        self.line_max.grid(row=2, column=3)
        
        # Long Pause Settings
        tk.Label(self.frame, text="Long Pause:").grid(row=3, column=0, sticky="e")
        self.long_min = tk.Entry(self.frame, width=5)
        self.long_min.insert(0, DEFAULT_PARAMS['long_pause_min'])
        self.long_min.grid(row=3, column=1)
        tk.Label(self.frame, text="to").grid(row=3, column=2)
        self.long_max = tk.Entry(self.frame, width=5)
        self.long_max.insert(0, DEFAULT_PARAMS['long_pause_max'])
        self.long_max.grid(row=3, column=3)
        tk.Label(self.frame, text="every").grid(row=3, column=4)
        self.long_freq = tk.Entry(self.frame, width=3)
        self.long_freq.insert(0, DEFAULT_PARAMS['long_pause_every'])
        self.long_freq.grid(row=3, column=5)
        tk.Label(self.frame, text="lines").grid(row=3, column=6)
        
        # Error Settings
        tk.Label(self.frame, text="Error Rate:").grid(row=4, column=0, sticky="e")
        self.error_rate = tk.Entry(self.frame, width=3)
        self.error_rate.insert(0, DEFAULT_PARAMS['error_rate'])
        self.error_rate.grid(row=4, column=1)
        tk.Label(self.frame, text="%").grid(row=4, column=2)
        tk.Label(self.frame, text="Correction:").grid(row=4, column=3, sticky="e")
        self.error_min = tk.Entry(self.frame, width=5)
        self.error_min.insert(0, DEFAULT_PARAMS['error_correction_min'])
        self.error_min.grid(row=4, column=4)
        tk.Label(self.frame, text="to").grid(row=4, column=5)
        self.error_max = tk.Entry(self.frame, width=5)
        self.error_max.insert(0, DEFAULT_PARAMS['error_correction_max'])
        self.error_max.grid(row=4, column=6)
        
        # Initial delay
        tk.Label(self.frame, text="Start Delay:").grid(row=5, column=0, sticky="e")
        self.initial_delay = tk.Entry(self.frame, width=5)
        self.initial_delay.insert(0, DEFAULT_PARAMS['initial_delay'])
        self.initial_delay.grid(row=5, column=1)
        tk.Label(self.frame, text="ms").grid(row=5, column=2)

def get_timing_params(controls):
    """Get current timing parameters from UI controls"""
    return {
        'char_delay': (int(controls.char_min.get()), int(controls.char_max.get())),
        'punctuation_extra': (int(controls.punct_min.get()), int(controls.punct_max.get())),
        'line_delay': (int(controls.line_min.get()), int(controls.line_max.get())),
        'long_pause': (int(controls.long_min.get()), int(controls.long_max.get())),
        'long_pause_every': int(controls.long_freq.get()),
        'error_rate': int(controls.error_rate.get()),
        'error_correction': (int(controls.error_min.get()), int(controls.error_max.get())),
        'initial_delay': int(controls.initial_delay.get())
    }

def start_typing():
    text = input_text.get("1.0", tk.END).rstrip()
    params = get_timing_params(timing_controls)
    
    if not text.strip():
        messagebox.showwarning("Empty Text", "Please enter some text to type.")
        return

    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    threading.Thread(target=type_text, args=(text, params)).start()
    start_timer()

def type_text(text, params):
    global stop_flag
    stop_flag = False
    lines = text.splitlines()
    
    # Convert all times from ms to seconds
    char_delay = (params['char_delay'][0]/1000, params['char_delay'][1]/1000)
    punct_extra = (params['punctuation_extra'][0]/1000, params['punctuation_extra'][1]/1000)
    line_delay = (params['line_delay'][0]/1000, params['line_delay'][1]/1000)
    long_pause = (params['long_pause'][0]/1000, params['long_pause'][1]/1000)
    error_correction = (params['error_correction'][0]/1000, params['error_correction'][1]/1000)
    
    # Initial delay to switch to target window
    time.sleep(params['initial_delay']/1000)
    
    line_count = 0

    for line in lines:
        if stop_flag:
            break

        # Random delay before starting each line
        time.sleep(random.uniform(*line_delay))

        for i, char in enumerate(line):
            if stop_flag:
                break
            
            # Simulate occasional errors
            if random.randint(1, 100) <= params['error_rate'] and i > 3:
                # Type wrong character
                wrong_char = chr(ord(char) + random.randint(-2, 2))
                pyautogui.write(wrong_char)
                time.sleep(random.uniform(*error_correction))
                # Backspace and correct
                pyautogui.press('backspace')
                time.sleep(random.uniform(error_correction[0]/2, error_correction[1]/2))
                pyautogui.write(char)
            
            # Type the character with random delay
            pyautogui.write(char)
            time.sleep(random.uniform(*char_delay))
            
            # Extra delay for punctuation
            if char in [".", "!", "?"]:
                time.sleep(random.uniform(*punct_extra))
            elif char in [",", ";", ":"]:
                time.sleep(random.uniform(punct_extra[0]/2, punct_extra[1]/2))

        # Don't press enter after last line
        if line_count < len(lines) - 1:
            pyautogui.press("enter")
            line_count += 1

            # Long pause every N lines
            if line_count % params['long_pause_every'] == 0:
                time.sleep(random.uniform(*long_pause))
            # Short pause for empty lines (paragraphs)
            elif line.strip() == "":
                time.sleep(random.uniform(line_delay[0]*1.5, line_delay[1]*1.5))

    stop_timer()
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

def stop_typing():
    global stop_flag
    stop_flag = True
    stop_timer()
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

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
root.geometry("750x750")
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

# Timing Controls
timing_controls = TimingControls(root)
timing_controls.frame.pack(pady=10, padx=10, fill=tk.X)

# Button Frame
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)

start_btn = tk.Button(button_frame, text="Start Typing", command=start_typing, 
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
        text="Note: All timing values are in milliseconds (1000ms = 1 second). Adjust the values to create unique typing patterns.",
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