"""
🔄 Username Rotator — Premium Edition
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Idle startup — rotation control via Telegram commands
Commands: .start .stop .on <acc> .off <acc> .list .status
"""

import asyncio

# ═══ Python 3.14 fix ═══
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# ═══════════════════════

import logging

# ═══ Quiet pyrogram spam ═══
logging.getLogger("pyrogram").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.connection").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.methods").setLevel(logging.CRITICAL)
# ═══════════════════════════

import sys
import signal
import time
from pathlib import Path

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import (
    AuthKeyUnregistered,
    UserDeactivated,
    SessionRevoked,
    FloodWait,
)

from config import (
    API_ID,
    API_HASH,
    SESSION_STRING,
    OWNER_ID,
    BOT_PREFIX,
)


# ═══════════════════════════════════════════════════
#  GLOBAL STATE
# ═══════════════════════════════════════════════════
START_TIME = time.time()
app = None
rotation_manager = None
_shutdown_event = None


# ═══════════════════════════════════════════════════
#  LOGGER
# ═══════════════════════════════════════════════════
def log(msg):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {msg}", flush=True)


# ═══════════════════════════════════════════════════
#  SESSION LOADER
# ═══════════════════════════════════════════════════
def get_session():
    if not SESSION_STRING:
        log("❌ SESSION_STRING missing in .env")
        sys.exit(1)

    if SESSION_STRING.startswith("gAAAAA"):
        try:
            from core.session_vault import SessionVault
            s = SessionVault().unlock(SESSION_STRING)
            log("🔐 Session unlocked")
            return s
        except Exception as e:
            log(f"❌ Unlock failed: {e}")
            sys.exit(1)

    log("⚠️  Plain session (not encrypted)")
    return SESSION_STRING


# ═══════════════════════════════════════════════════
#  CLIENT
# ═══════════════════════════════════════════════════
def create_main_client():
    return Client(
        "main_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=get_session(),
        parse_mode=ParseMode.HTML,
        workers=10,
    )


# ═══════════════════════════════════════════════════
#  BANNER
# ═══════════════════════════════════════════════════
def print_banner():
    print(f"""
╔══════════════════════════════════════════════╗
║   🔄  USERNAME ROTATOR                    🔄
║   Prefix: {BOT_PREFIX:<34} ║
║   Owner:  {str(OWNER_ID):<34} ║
║   Mode:   IDLE (waiting for .start)          ║
╚══════════════════════════════════════════════╝
""")


# ═══════════════════════════════════════════════════
#  STARTUP
# ═══════════════════════════════════════════════════
async def startup():
    global rotation_manager

    print_banner()
    log("🚀 Starting userbot...")

    # ─── Start Pyrogram ───
    try:
        await app.start()
    except AuthKeyUnregistered:
        log("❌ Session revoked! Generate new SESSION_STRING.")
        sys.exit(1)
    except UserDeactivated:
        log("❌ Account deactivated!")
        sys.exit(1)
    except SessionRevoked:
        log("❌ Session revoked!")
        sys.exit(1)
    except Exception as e:
        log(f"❌ Failed to start: {e}")
        sys.exit(1)

    me = await app.get_me()
    log(f"✅ Logged in as: {me.first_name} (@{me.username})")

    if me.id != OWNER_ID:
        log(f"⚠️  OWNER_ID mismatch: env={OWNER_ID} actual={me.id}")

    # ─── Load modules ───
    log("📦 Loading modules...")
    try:
        from modules import commands
        commands.register(app)
        log("✅ Modules loaded")
    except Exception as e:
        log(f"⚠️  Module load failed: {e}")

    # ─── Load accounts (IDLE mode) ───
    log("🔄 Loading accounts (IDLE mode)...")
    try:
        from core.rotation_manager import RotationManager
        rotation_manager = RotationManager(app)
        await rotation_manager.load_accounts()

        loaded = len(rotation_manager.accounts)
        if loaded:
            log(f"✅ {loaded} accounts loaded (IDLE)")
        else:
            log("⚠️  No accounts loaded")
    except Exception as e:
        log(f"❌ Rotation manager failed: {e}")
        rotation_manager = None

    # ─── Notify owner ───
    try:
        rm_status = ""
        if rotation_manager:
            gs = rotation_manager.get_global_status()
            rm_status = (
                f"\n👥 Accounts: <code>{gs['accounts_loaded']}/{gs['total_accounts']}</code>"
                f"\n📢 Channels: <code>0</code>"
                f"\n🎮 Mode: <b>IDLE</b>"
            )

        await app.send_message(
            OWNER_ID,
            f"🚀 <b>Username Rotator online!</b>\n\n"
            f"👤 {me.mention}"
            f"{rm_status}\n\n"
            f"<i>Use <code>.start</code> to begin</i>\n"
            f"<i>Use <code>.on sakil1</code> for one account</i>\n"
            f"<i>Use <code>.help</code> for commands</i>"
        )
        log("📨 Owner notified")
    except Exception as e:
        log(f"⚠️  Notify failed: {e}")

    log("✅ Ready — waiting for commands")


# ═══════════════════════════════════════════════════
#  SHUTDOWN
# ═══════════════════════════════════════════════════
async def shutdown(sig=None):
    global _shutdown_event
    if _shutdown_event is None or _shutdown_event.is_set():
        return
    _shutdown_event.set()

    log(f"🛑 Shutting down (signal={sig})...")

    try:
        if rotation_manager:
            await rotation_manager.shutdown_all()
            log("✅ Accounts logged out")

        if app and app.is_connected:
            try:
                await app.send_message(OWNER_ID, "🔴 <b>Userbot stopped.</b>")
            except Exception:
                pass
            await app.stop()
            log("✅ Client stopped")
    except Exception as e:
        log(f"❌ Shutdown error: {e}")

    log("👋 Goodbye!")


def signal_handler(sig, frame):
    log(f"📡 Signal: {sig}")
    if _shutdown_event is not None:
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(shutdown(sig))
        except Exception:
            pass


# ═══════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════
async def main():
    global app, _shutdown_event

    _shutdown_event = asyncio.Event()

    # Signal handlers
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    except Exception:
        pass

    # Create client
    app = create_main_client()

    # Startup
    await startup()

    # Keep running
    try:
        await _shutdown_event.wait()
    except asyncio.CancelledError:
        await shutdown()


# ═══════════════════════════════════════════════════
#  CRASH RECOVERY
# ═══════════════════════════════════════════════════
def run_with_recovery():
    max_retries = 5
    delay = 10

    for attempt in range(1, max_retries + 1):
        try:
            asyncio.run(main())
            break
        except KeyboardInterrupt:
            log("⌨️  Interrupted")
            break
        except Exception as e:
            log(f"💥 Crash ({attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                log(f"⏳ Restart in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                log("❌ Max retries reached.")
                sys.exit(1)


# ═══════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    # Create folders
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("accounts").mkdir(exist_ok=True)

    try:
        run_with_recovery()
    except KeyboardInterrupt:
        log("👋 Bye")
