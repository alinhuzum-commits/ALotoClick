"""Autoclicker package.

Provides a simple, cross-platform autoclicker with CLI and optional GUI.
"""

__all__ = ["AutoClicker"]
__version__ = "0.1.0"

# Lazy import in CLI avoids importing pynput during --help
try:
    from .clicker import AutoClicker  # noqa: F401
except Exception:  # pragma: no cover - import may fail in headless help usage
    # Defer errors until runtime when actually needed
    AutoClicker = None  # type: ignore
