"""
🔧 Helper Utilities
Commands ke liye shared functions
"""

import time
from datetime import datetime
from core.colors import C


def cmd_filter(name, prefixes="."):
    """Quick command filter."""
    from pyrogram import filters
    return filters.command(name, prefixes=prefixes) & filters.me


def format_uptime(seconds):
    """Format seconds to human readable."""
    sec = int(seconds)
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)

    if h > 0:
        return f"{h}h {m}m {s}s"
    if m > 0:
        return f"{m}m {s}s"
    return f"{s}s"


def format_time(ts):
    """Format timestamp."""
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S")


def progress_bar(current, total, width=15):
    """ASCII progress bar."""
    if total == 0:
        return "░" * width
    filled = int(width * (current / total))
    return "█" * filled + "░" * (width - filled)


def truncate(text, length=30):
    """Truncate long strings."""
    text = str(text)
    if len(text) <= length:
        return text
    return text[:length - 3] + "..."


def make_html_safe(text):
    """Escape HTML characters."""
    text = str(text)
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def split_chunks(items, chunk_size=10):
    """Split list into chunks."""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def humanize_number(n):
    """Format large numbers: 1000 → 1K."""
    n = int(n)
    for unit in ["", "K", "M", "B"]:
        if abs(n) < 1000:
            return f"{n}{unit}"
        n //= 1000
    return f"{n}T"


def emoji_status(ok):
    """Return emoji for status."""
    return "✅" if ok else "❌"


def safe_int(value, default=0):
    """Safely convert to int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def parse_duration(s):
    """Parse '30m', '2h', '1d' to seconds."""
    import re
    m = re.match(r"^(\d+)([smhd])$", s.lower())
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2)
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return n * multipliers[unit]
