from __future__ import annotations

import argparse
import sys
import threading
from typing import Optional


def _positive_float(value: str) -> float:
    try:
        v = float(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if v <= 0:
        raise argparse.ArgumentTypeError("must be > 0")
    return v


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autoclicker",
        description="Simple cross-platform autoclicker with global hotkey toggle.",
    )
    parser.add_argument(
        "--cps",
        type=_positive_float,
        default=10.0,
        help="Clicks per second (default: 10.0)",
    )
    parser.add_argument(
        "--button",
        choices=["left", "right", "middle"],
        default="left",
        help="Mouse button to click (default: left)",
    )
    parser.add_argument(
        "--hotkey",
        default="<f6>",
        help=(
            "Global hotkey for toggle, in pynput format (e.g. '<f6>', "
            "'<ctrl>+<alt>+c>'). Default: <f6>"
        ),
    )
    parser.add_argument(
        "--exit-hotkey",
        default="<esc>",
        help="Global hotkey to exit program. Default: <esc>",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch simple Tkinter GUI instead of CLI mode",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    # Parse first so `--help` exits before importing heavy deps
    args = parser.parse_args(argv)

    if args.gui:
        # Lazy import to avoid requiring tkinter unless GUI requested
        from .gui import run_gui
        run_gui(initial_cps=args.cps, button=args.button)
        return

    # Lazy import so help does not require pynput in headless envs
    from .clicker import AutoClicker
    from pynput import keyboard

    clicker = AutoClicker(clicks_per_second=args.cps, button=args.button)

    stop_event = threading.Event()

    def on_toggle() -> None:
        enabled = clicker.toggle()
        state = "ON" if enabled else "OFF"
        print(f"[autoclicker] Toggled: {state} (cps={clicker.clicks_per_second:.2f})", flush=True)

    def on_exit() -> None:
        print("[autoclicker] Exiting...", flush=True)
        stop_event.set()

    hotkey_map = {args.hotkey: on_toggle, args.exit_hotkey: on_exit}

    print(
        "[autoclicker] Ready. Toggle with",
        args.hotkey,
        "| Exit with",
        args.exit_hotkey,
        "| Button:",
        args.button,
        f"| CPS: {args.cps:.2f}",
        flush=True,
    )

    # Ensure worker thread is present so first toggle is instant
    clicker.disable()

    # Start hotkey listener loop
    try:
        with keyboard.GlobalHotKeys(hotkey_map) as listener:
            while not stop_event.wait(timeout=0.1):
                pass
            listener.stop()
    except KeyboardInterrupt:
        pass
    finally:
        clicker.shutdown()
        sys.exit(0)
