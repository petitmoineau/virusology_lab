#!/usr/bin/env python
# coding: utf-8

# In[1]:


import subprocess
import os
import tkinter as tk
from tkinter import scrolledtext
import threading
import random
import pyautogui
import re

def process_nslookup_output(output):
    """
    Extract the second IP address from the nslookup command output.
    
    :param output: Output from the nslookup command.
    :type output: str
    :return: Extracted IP address.
    :rtype: str
    """
    ip_addresses = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', output)
    if len(ip_addresses) > 1:
        return ip_addresses[1]
    return "IP not found"

def run_command(cmd):
    """
    Run a command in CMD.
    
    :param cmd: Command to run.
    :type cmd: str
    """
    try:
        result = subprocess.check_output(["cmd", "/c", cmd], stderr=subprocess.STDOUT, universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return e.output  # If the command has a non-zero exit, return its output anyway.

def get_best_move(x, y, width, height, screen_width, screen_height):
    # Check all four directions and pick the one that maximizes the distance
    distances = [
        (x, 0),  # top
        (0, y),  # left
        (screen_width - width, y),  # right
        (x, screen_height - height)  # bottom
    ]
    return max(distances, key=lambda pos: ((pos[0] - x) ** 2 + (pos[1] - y) ** 2) ** 0.5)

def show_dialog(title, text):
    root = tk.Tk()
    root.title(title)
    root.geometry("650x400")
    root.attributes('-topmost', True)
    root.configure(bg='red') 

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    TITLE_BAR_HEIGHT = 30  # An estimated value; you may need to adjust this

    def move_away():
        x, y = pyautogui.position()  # Get mouse cursor position
        window_x = root.winfo_x()
        window_y = root.winfo_y() - TITLE_BAR_HEIGHT

    # If mouse is inside window bounds, including the title bar, move window
        if window_x < x < window_x + 600 and window_y < y < window_y + 400 + TITLE_BAR_HEIGHT:
            new_x, new_y = get_best_move(x, y, 600, 400, screen_width, screen_height)
            root.geometry(f"+{new_x}+{new_y}")
        root.after(1, move_away)
        
    # Periodically check mouse position and move the window away if needed
    def move_away():
        x, y = pyautogui.position()  # Get mouse cursor position
        window_x = root.winfo_x()
        window_y = root.winfo_y()

        # If mouse is inside window bounds, move window
        if window_x < x < window_x + 600 and window_y < y < window_y + 400:
            new_x, new_y = get_best_move(x, y, 600, 400, screen_width, screen_height)
            root.geometry(f"+{new_x}+{new_y}")

        root.after(1, move_away)  # Check again after 10 milliseconds

    move_away()  # Start the move_away function

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, bg='red', fg='white')
    text_widget.insert(tk.END, text)
    text_widget.grid(column=0, row=0, sticky="W")
    text_widget.config(state=tk.DISABLED)
    
    def alternate_color():
        current_color = root.cget("bg")
        new_color = "black" if current_color == "red" else "red"
        root.configure(bg=new_color)
        text_widget.configure(bg=new_color)
        root.after(100, alternate_color)

    alternate_color()

    root.mainloop()

if __name__ == "__main__":
    log_file = "output_log.txt"
    
    command_to_run1 = "nslookup myip.opendns.com resolver1.opendns.com"
    raw_output1 = run_command(command_to_run1)
    raw_output2 = "nothing"
    
    current_directory = os.getcwd()
    nmap_path = os.path.join(current_directory, ".\\Nmap\\nmap.exe")
    if os.path.exists(nmap_path):
        command_to_run2 = f"{nmap_path} scanme.nmap.org"
        raw_output2 = run_command(command_to_run2)
    
    with open(log_file, "w") as file:
        file.write("1:\n")
        file.write(raw_output1)
        file.write("\n2:\n")
        file.write(raw_output2)
    
    output_phrase = "hello you dumb idiot you are exposed\nwe scanned your ports\nand already have stolen everything you\nhave on your computer haha,\nthis is your public IP:\n "
    output_phrase += process_nslookup_output(raw_output1)
    
    for _ in range(1):
        t = threading.Thread(target=show_dialog, args=("WARNING HAHAHAHAHA", output_phrase))
        t.start()

