"""
🌈 Terminal Color Codes
Premium output ke liye
"""


class C:
    """ANSI color palette."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Standard colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Backgrounds
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Premium 256-color palette
    PURPLE = "\033[38;5;141m"
    PINK = "\033[38;5;213m"
    TEAL = "\033[38;5;79m"
    ORANGE = "\033[38;5;208m"
    GOLD = "\033[38;5;220m"


def colorize(text, *codes):
    """Apply color codes to text."""
    return "".join(codes) + text + C.RESET


# ═══════════════════════════════════════════
#  Quick shortcuts
# ═══════════════════════════════════════════

def success(text):
    return f"{C.BRIGHT_GREEN}✅ {text}{C.RESET}"


def error(text):
    return f"{C.BRIGHT_RED}❌ {text}{C.RESET}"


def warning(text):
    return f"{C.BRIGHT_YELLOW}⚠️  {text}{C.RESET}"


def info(text):
    return f"{C.BRIGHT_CYAN}ℹ️  {text}{C.RESET}"


def premium(text):
    return f"{C.PURPLE}{C.BOLD}{text}{C.RESET}"


def accent(text):
    return f"{C.PINK}{C.BOLD}{text}{C.RESET}"


def dim(text):
    return f"{C.DIM}{text}{C.RESET}"
