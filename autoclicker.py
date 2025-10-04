#!/usr/bin/env python3
"""
Aplicație AutoClicker - O aplicație simplă pentru automatizarea click-urilor de mouse
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pynput import mouse
from pynput.mouse import Button, Listener
import sys

class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AutoClicker")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Variabile pentru controlul aplicației
        self.is_clicking = False
        self.click_thread = None
        self.target_x = 0
        self.target_y = 0
        self.click_interval = 1.0
        self.click_count = 0
        self.max_clicks = 0  # 0 = infinit
        self.mouse_controller = mouse.Controller()
        self.position_listener = None
        
        self.setup_ui()
        self.setup_hotkeys()
        
    def setup_ui(self):
        """Configurează interfața grafică"""
        # Titlu principal
        title_label = tk.Label(self.root, text="🖱️ AutoClicker", 
                              font=("Arial", 16, "bold"), fg="#2c3e50")
        title_label.pack(pady=10)
        
        # Frame pentru poziția mouse-ului
        position_frame = ttk.LabelFrame(self.root, text="Poziția Click-ului", padding=10)
        position_frame.pack(fill="x", padx=20, pady=5)
        
        # Afișarea coordonatelor
        self.position_label = tk.Label(position_frame, text=f"X: {self.target_x}, Y: {self.target_y}",
                                      font=("Arial", 10))
        self.position_label.pack()
        
        # Buton pentru selectarea poziției
        select_pos_btn = tk.Button(position_frame, text="📍 Selectează Poziția",
                                  command=self.select_position, bg="#3498db", fg="white",
                                  font=("Arial", 10, "bold"))
        select_pos_btn.pack(pady=5)
        
        # Frame pentru setări
        settings_frame = ttk.LabelFrame(self.root, text="Setări Click", padding=10)
        settings_frame.pack(fill="x", padx=20, pady=5)
        
        # Interval între click-uri
        tk.Label(settings_frame, text="Interval (secunde):").pack(anchor="w")
        self.interval_var = tk.DoubleVar(value=1.0)
        interval_scale = tk.Scale(settings_frame, from_=0.1, to=10.0, resolution=0.1,
                                 orient="horizontal", variable=self.interval_var)
        interval_scale.pack(fill="x", pady=5)
        
        # Numărul de click-uri
        tk.Label(settings_frame, text="Numărul de click-uri (0 = infinit):").pack(anchor="w")
        self.clicks_var = tk.IntVar(value=0)
        clicks_entry = tk.Entry(settings_frame, textvariable=self.clicks_var)
        clicks_entry.pack(fill="x", pady=5)
        
        # Tipul de click
        tk.Label(settings_frame, text="Tipul de click:").pack(anchor="w")
        self.click_type_var = tk.StringVar(value="left")
        click_type_frame = tk.Frame(settings_frame)
        click_type_frame.pack(fill="x", pady=5)
        
        tk.Radiobutton(click_type_frame, text="Click Stânga", variable=self.click_type_var,
                      value="left").pack(side="left")
        tk.Radiobutton(click_type_frame, text="Click Dreapta", variable=self.click_type_var,
                      value="right").pack(side="left")
        tk.Radiobutton(click_type_frame, text="Click Mijloc", variable=self.click_type_var,
                      value="middle").pack(side="left")
        
        # Frame pentru control
        control_frame = ttk.LabelFrame(self.root, text="Control", padding=10)
        control_frame.pack(fill="x", padx=20, pady=5)
        
        # Butoane de control
        button_frame = tk.Frame(control_frame)
        button_frame.pack(fill="x")
        
        self.start_btn = tk.Button(button_frame, text="▶️ Start", command=self.start_clicking,
                                  bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
        self.start_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.stop_btn = tk.Button(button_frame, text="⏹️ Stop", command=self.stop_clicking,
                                 bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                                 state="disabled")
        self.stop_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        # Statistici
        stats_frame = ttk.LabelFrame(self.root, text="Statistici", padding=10)
        stats_frame.pack(fill="x", padx=20, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Click-uri efectuate: 0",
                                   font=("Arial", 10))
        self.stats_label.pack()
        
        # Instrucțiuni
        instructions_frame = ttk.LabelFrame(self.root, text="Instrucțiuni", padding=10)
        instructions_frame.pack(fill="x", padx=20, pady=5)
        
        instructions_text = """
• Apasă 'Selectează Poziția' și click pe locul dorit
• Setează intervalul și numărul de click-uri
• Apasă 'Start' pentru a începe
• Apasă 'Stop' sau ESC pentru a opri
• F1 - Start/Stop rapid
        """
        instructions_label = tk.Label(instructions_frame, text=instructions_text,
                                     justify="left", font=("Arial", 9))
        instructions_label.pack()
        
    def setup_hotkeys(self):
        """Configurează hotkey-urile globale"""
        def on_key_press(key):
            try:
                if hasattr(key, 'char'):
                    return
                    
                if key == key.esc:
                    if self.is_clicking:
                        self.stop_clicking()
                elif key == key.f1:
                    if self.is_clicking:
                        self.stop_clicking()
                    else:
                        self.start_clicking()
            except AttributeError:
                pass
        
        # Pornește listener-ul pentru taste în thread separat
        from pynput import keyboard
        self.key_listener = keyboard.Listener(on_press=on_key_press)
        self.key_listener.start()
        
    def select_position(self):
        """Permite utilizatorului să selecteze poziția pentru click"""
        messagebox.showinfo("Selectare Poziție", 
                           "Click pe locul unde vrei să se facă click-urile automate.\n"
                           "Apasă ESC pentru a anula.")
        
        def on_click(x, y, button, pressed):
            if pressed and button == Button.left:
                self.target_x = x
                self.target_y = y
                self.position_label.config(text=f"X: {x}, Y: {y}")
                return False  # Oprește listener-ul
        
        # Minimizează fereastra temporar
        self.root.withdraw()
        
        # Pornește listener-ul pentru mouse
        with Listener(on_click=on_click) as listener:
            listener.join()
        
        # Restaurează fereastra
        self.root.deiconify()
        self.root.lift()
        
    def start_clicking(self):
        """Pornește procesul de click automat"""
        if self.target_x == 0 and self.target_y == 0:
            messagebox.showwarning("Atenție", "Te rog selectează mai întâi poziția pentru click!")
            return
        
        self.is_clicking = True
        self.click_count = 0
        self.click_interval = self.interval_var.get()
        self.max_clicks = self.clicks_var.get()
        
        # Actualizează interfața
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        # Pornește thread-ul pentru clicking
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()
        
    def stop_clicking(self):
        """Oprește procesul de click automat"""
        self.is_clicking = False
        
        # Actualizează interfața
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
    def click_loop(self):
        """Loop-ul principal pentru click-uri automate"""
        while self.is_clicking:
            # Verifică dacă am ajuns la numărul maxim de click-uri
            if self.max_clicks > 0 and self.click_count >= self.max_clicks:
                break
            
            # Efectuează click-ul
            try:
                button_map = {
                    'left': Button.left,
                    'right': Button.right,
                    'middle': Button.middle
                }
                
                button = button_map.get(self.click_type_var.get(), Button.left)
                self.mouse_controller.position = (self.target_x, self.target_y)
                self.mouse_controller.click(button)
                
                self.click_count += 1
                
                # Actualizează statisticile în thread-ul principal
                self.root.after(0, self.update_stats)
                
            except Exception as e:
                print(f"Eroare la click: {e}")
            
            # Așteaptă intervalul specificat
            time.sleep(self.click_interval)
        
        # Oprește clicking-ul când se termină
        self.root.after(0, self.stop_clicking)
        
    def update_stats(self):
        """Actualizează statisticile afișate"""
        self.stats_label.config(text=f"Click-uri efectuate: {self.click_count}")
        
    def on_closing(self):
        """Gestionează închiderea aplicației"""
        self.is_clicking = False
        if hasattr(self, 'key_listener'):
            self.key_listener.stop()
        self.root.destroy()
        
    def run(self):
        """Pornește aplicația"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = AutoClicker()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicația a fost oprită de utilizator.")
    except Exception as e:
        print(f"Eroare: {e}")
        messagebox.showerror("Eroare", f"A apărut o eroare: {e}")