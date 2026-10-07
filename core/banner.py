"""
🎨 Premium ASCII Banner
Startup aur sections ke liye
"""

from core.colors import C


def show_banner(version="2.0", owner_id=0, prefix=".", accounts=0, channels=0):
    """Display premium startup banner."""

    banner = f"""{C.PURPLE}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  {C.PINK}██████╗  ██████╗ ████████╗ █████╗ ████████╗ ███████╗{C.PURPLE}          ║
║  {C.PINK}██╔══██╗██╔═══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝{C.PURPLE}          ║
║  {C.PINK}██████╔╝██║   ██║   ██║   ███████║   ██║   █████╗{C.PURPLE}            ║
║  {C.PINK}██╔══██╗██║   ██║   ██║   ██╔══██║   ██║   ██╔══╝{C.PURPLE}            ║
║  {C.PINK}██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ███████╗{C.PURPLE}          ║
║  {C.PINK}╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝{C.PURPLE}          ║
║                                                                   ║
║  {C.BOLD}{C.PINK}⚡ Multi-Account Username Rotation Engine ⚡{C.RESET}{C.PURPLE}              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{C.RESET}

  {C.DIM}Version   {C.RESET}{C.PINK}v{version}{C.RESET}
  {C.DIM}Owner     {C.RESET}{C.PINK}{owner_id}{C.RESET}
  {C.DIM}Prefix    {C.RESET}{C.PINK}{prefix}{C.RESET}
  {C.DIM}Accounts  {C.RESET}{C.BRIGHT_GREEN}{accounts}{C.RESET}
  {C.DIM}Channels  {C.RESET}{C.BRIGHT_GREEN}{channels}{C.RESET}
  {C.DIM}Engine    {C.RESET}{C.BRIGHT_CYAN}Pyrogram • MTProto{C.RESET}
"""
    print(banner)


def show_section(title, icon="◆"):
    """Section divider with title."""
    print(f"\n{C.PURPLE}{icon * 2} {C.BOLD}{title}{C.RESET} {C.PURPLE}{icon * 2}{C.RESET}")


def show_divider(char="─", length=68, color=C.DIM):
    """Horizontal divider."""
    print(f"{color}{char * length}{C.RESET}")


def show_box(title, content, color=C.PURPLE):
    """Display content in a box."""
    width = 65
    print(f"\n{color}┌{'─' * width}┐{C.RESET}")
    print(f"{color}│{C.RESET} {C.BOLD}{title:<{width - 2}}{C.RESET} {color}│{C.RESET}")
    print(f"{color}├{'─' * width}┤{C.RESET}")
    for line in content.split("\n"):
        print(f"{color}│{C.RESET} {line:<{width - 2}} {color}│{C.RESET}")
    print(f"{color}└{'─' * width}┘{C.RESET}")


def show_progress(current, total, width=30):
    """Show progress bar."""
    if total == 0:
        pct = 0
    else:
        pct = current / total
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"{C.PURPLE}{bar}{C.RESET} {C.PINK}{int(pct * 100)}%{C.RESET}"
