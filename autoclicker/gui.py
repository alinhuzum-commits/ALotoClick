from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Literal


def run_gui(initial_cps: float = 10.0, button: Literal["left", "right", "middle"] = "left") -> None:
    from .clicker import AutoClicker

    clicker = AutoClicker(clicks_per_second=initial_cps, button=button)

    root = tk.Tk()
    root.title("Autoclicker")
    root.geometry("320x220")

    cps_var = tk.DoubleVar(value=initial_cps)
    status_var = tk.StringVar(value="OFF")
    button_var = tk.StringVar(value=button)

    def update_cps(*_args) -> None:
        try:
            clicker.set_clicks_per_second(float(cps_var.get()))
        except Exception:
            pass

    def toggle() -> None:
        enabled = clicker.toggle()
        status_var.set("ON" if enabled else "OFF")
        toggle_btn.configure(text="Stop" if enabled else "Start")

    def on_close() -> None:
        clicker.shutdown()
        root.destroy()

    # Controls
    frm = ttk.Frame(root, padding=12)
    frm.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frm, text="Clicks per second:").pack(anchor=tk.W)
    cps_spin = ttk.Spinbox(frm, from_=0.1, to=100.0, increment=0.1, textvariable=cps_var, width=10)
    cps_spin.pack(anchor=tk.W, pady=(0, 8))
    cps_var.trace_add("write", update_cps)

    ttk.Label(frm, text="Mouse button:").pack(anchor=tk.W)
    btn_combo = ttk.Combobox(frm, values=["left", "right", "middle"], textvariable=button_var, state="readonly")
    btn_combo.pack(anchor=tk.W, pady=(0, 8))

    def on_button_changed(_event) -> None:
        # Recreate clicker with new button selection
        nonlocal clicker
        was_enabled = clicker.is_enabled
        clicker.shutdown()
        clicker = AutoClicker(clicks_per_second=float(cps_var.get()), button=button_var.get())
        if was_enabled:
            clicker.enable()

    btn_combo.bind("<<ComboboxSelected>>", on_button_changed)

    toggle_btn = ttk.Button(frm, text="Start", command=toggle)
    toggle_btn.pack(fill=tk.X, pady=(4, 8))

    status_row = ttk.Frame(frm)
    status_row.pack(fill=tk.X)
    ttk.Label(status_row, text="Status:").pack(side=tk.LEFT)
    ttk.Label(status_row, textvariable=status_var, foreground="#0a7", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=(6, 0))

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
