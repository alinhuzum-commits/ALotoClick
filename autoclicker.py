#!/usr/bin/env python3
"""
Autoclicker Application
A simple autoclicker with GUI interface
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode


class AutoClicker:
    def __init__(self):
        self.clicking = False
        self.mouse = MouseController()
        self.click_interval = 1.0
        self.click_button = Button.left
        self.click_type = "single"
        self.toggle_key = KeyCode.from_char('s')
        
    def toggle_clicking(self):
        """Toggle clicking on/off"""
        self.clicking = not self.clicking
        
    def click_loop(self):
        """Main clicking loop"""
        while True:
            if self.clicking:
                self.mouse.click(self.click_button, 1 if self.click_type == "single" else 2)
                time.sleep(self.click_interval)
            else:
                time.sleep(0.1)


class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        self.autoclicker = AutoClicker()
        self.keyboard_listener = None
        
        self.setup_ui()
        self.start_click_thread()
        self.start_keyboard_listener()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="AutoClicker", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Click interval
        interval_label = ttk.Label(main_frame, text="Click Interval (seconds):")
        interval_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.interval_var = tk.DoubleVar(value=1.0)
        interval_spinbox = ttk.Spinbox(
            main_frame,
            from_=0.001,
            to=60.0,
            increment=0.1,
            textvariable=self.interval_var,
            width=15,
            command=self.update_interval
        )
        interval_spinbox.grid(row=1, column=1, sticky=tk.W, pady=5)
        interval_spinbox.bind('<Return>', lambda e: self.update_interval())
        
        # Mouse button selection
        button_label = ttk.Label(main_frame, text="Mouse Button:")
        button_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.button_var = tk.StringVar(value="Left")
        button_combo = ttk.Combobox(
            main_frame,
            textvariable=self.button_var,
            values=["Left", "Right", "Middle"],
            state="readonly",
            width=13
        )
        button_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        button_combo.bind("<<ComboboxSelected>>", self.update_button)
        
        # Click type selection
        type_label = ttk.Label(main_frame, text="Click Type:")
        type_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.type_var = tk.StringVar(value="Single")
        type_combo = ttk.Combobox(
            main_frame,
            textvariable=self.type_var,
            values=["Single", "Double"],
            state="readonly",
            width=13
        )
        type_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        type_combo.bind("<<ComboboxSelected>>", self.update_type)
        
        # Hotkey selection
        hotkey_label = ttk.Label(main_frame, text="Toggle Hotkey:")
        hotkey_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.hotkey_var = tk.StringVar(value="s")
        hotkey_entry = ttk.Entry(main_frame, textvariable=self.hotkey_var, width=15)
        hotkey_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        hotkey_entry.bind('<KeyRelease>', self.update_hotkey)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Status: Stopped",
            font=("Arial", 12, "bold"),
            foreground="red"
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Start/Stop button
        self.toggle_button = ttk.Button(
            main_frame,
            text="Start (or press 's')",
            command=self.toggle_clicking,
            width=20
        )
        self.toggle_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Info label
        info_label = ttk.Label(
            main_frame,
            text="Press the hotkey to start/stop clicking",
            font=("Arial", 9),
            foreground="gray"
        )
        info_label.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
    def update_interval(self):
        """Update click interval"""
        try:
            interval = self.interval_var.get()
            if interval > 0:
                self.autoclicker.click_interval = interval
        except:
            pass
    
    def update_button(self, event=None):
        """Update mouse button"""
        button_map = {
            "Left": Button.left,
            "Right": Button.right,
            "Middle": Button.middle
        }
        self.autoclicker.click_button = button_map.get(self.button_var.get(), Button.left)
    
    def update_type(self, event=None):
        """Update click type"""
        self.autoclicker.click_type = self.type_var.get().lower()
    
    def update_hotkey(self, event=None):
        """Update toggle hotkey"""
        key = self.hotkey_var.get()
        if key and len(key) == 1:
            self.autoclicker.toggle_key = KeyCode.from_char(key.lower())
            self.toggle_button.config(text=f"Start (or press '{key.lower()}')")
    
    def toggle_clicking(self):
        """Toggle clicking on/off"""
        self.autoclicker.toggle_clicking()
        self.update_status()
    
    def update_status(self):
        """Update status label"""
        if self.autoclicker.clicking:
            self.status_label.config(text="Status: Running", foreground="green")
            self.toggle_button.config(text=f"Stop (or press '{self.hotkey_var.get()}')")
        else:
            self.status_label.config(text="Status: Stopped", foreground="red")
            self.toggle_button.config(text=f"Start (or press '{self.hotkey_var.get()}')")
    
    def start_click_thread(self):
        """Start the clicking thread"""
        click_thread = threading.Thread(target=self.autoclicker.click_loop, daemon=True)
        click_thread.start()
    
    def on_press(self, key):
        """Handle keyboard press"""
        try:
            if key == self.autoclicker.toggle_key:
                self.toggle_clicking()
        except AttributeError:
            pass
    
    def start_keyboard_listener(self):
        """Start keyboard listener"""
        self.keyboard_listener = Listener(on_press=self.on_press)
        self.keyboard_listener.start()
    
    def on_closing(self):
        """Handle window closing"""
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AutoClickerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
