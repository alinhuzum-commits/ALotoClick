from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional

from pynput.mouse import Button, Controller


_BUTTON_MAP = {
    "left": Button.left,
    "right": Button.right,
    "middle": Button.middle,
}


@dataclass
class ClickerConfig:
    clicks_per_second: float = 10.0
    button_name: str = "left"  # one of left|right|middle


class AutoClicker:
    """Threaded autoclicker controlled via enable/disable/toggle.

    Use `enable()` to start clicking, `disable()` to stop, and `shutdown()` to
    stop the worker thread entirely.
    """

    def __init__(self, clicks_per_second: float = 10.0, button: str = "left") -> None:
        if clicks_per_second <= 0:
            raise ValueError("clicks_per_second must be > 0")
        if button not in _BUTTON_MAP:
            raise ValueError("button must be one of: left, right, middle")

        self._mouse_controller = Controller()
        self._button: Button = _BUTTON_MAP[button]
        self._clicks_per_second: float = float(clicks_per_second)

        self._should_click_event = threading.Event()
        self._stop_worker_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._state_lock = threading.Lock()

    # ----- Public API -----
    @property
    def is_enabled(self) -> bool:
        return self._should_click_event.is_set()

    @property
    def clicks_per_second(self) -> float:
        return self._clicks_per_second

    def set_clicks_per_second(self, clicks_per_second: float) -> None:
        if clicks_per_second <= 0:
            raise ValueError("clicks_per_second must be > 0")
        with self._state_lock:
            self._clicks_per_second = float(clicks_per_second)

    def enable(self) -> None:
        """Begin clicking (spawns worker if needed)."""
        self._ensure_worker()
        self._should_click_event.set()

    def disable(self) -> None:
        """Pause clicking but keep worker alive for fast toggling."""
        self._should_click_event.clear()

    def toggle(self) -> bool:
        """Toggle clicking on/off. Returns new enabled state."""
        if self.is_enabled:
            self.disable()
        else:
            self.enable()
        return self.is_enabled

    def shutdown(self) -> None:
        """Stop clicking and terminate the worker thread."""
        self._should_click_event.clear()
        self._stop_worker_event.set()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)

    # ----- Internals -----
    def _ensure_worker(self) -> None:
        if self._worker_thread and self._worker_thread.is_alive():
            return
        self._stop_worker_event.clear()
        self._worker_thread = threading.Thread(
            target=self._worker_loop, name="AutoClickerWorker", daemon=True
        )
        self._worker_thread.start()

    def _compute_interval_seconds(self) -> float:
        with self._state_lock:
            cps = self._clicks_per_second
        return max(1.0 / cps, 0.0005)

    def _worker_loop(self) -> None:
        # Wait loop: sleep briefly when not enabled to keep CPU low
        try:
            while not self._stop_worker_event.is_set():
                if not self._should_click_event.wait(timeout=0.1):
                    continue

                # Clicking loop while enabled
                while self._should_click_event.is_set() and not self._stop_worker_event.is_set():
                    try:
                        self._mouse_controller.click(self._button, 1)
                    except Exception:
                        # Swallow transient backend errors to keep the loop alive
                        pass
                    time.sleep(self._compute_interval_seconds())
        finally:
            # Ensure not clicking when worker exits
            self._should_click_event.clear()
