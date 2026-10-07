"""
🔄 Username Rotator — Premium Edition
"""

import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import logging
logging.getLogger("pyrogram").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.connection").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.CRITICAL)

import sys
import signal
from pathlib import Path

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import AuthKeyUnregistered, UserDeactivated, SessionRevoked

from config import API_ID, API_HASH, SESSION_STRING, OWNER_ID, BOT_PREFIX


app = None
rotation_manager = None
_shutdown_event = None


def log(msg):
    import time
    t = time.strftime("%H:%M:%S")
    print(f"{t} | {msg}", flush=True)


def get_session():
    if not SESSION_STRING:
        print("❌ SESSION_STRING missing")
        sys.exit(1)

    if SESSION_STRING.startswith("gAAAAA"):
        try:
            from core.session_vault import SessionVault
            s = SessionVault().unlock(SESSION_STRING)
            log("🔐 Session unlocked")
            return s
        except Exception as e:
            print(f"❌ Unlock failed: {e}")
            sys.exit(1)

    return SESSION_STRING


def create_main_client():
    return Client(
        "main_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=get_session(),
        parse_mode=ParseMode.HTML,
        workers=10,
    )


async def startup():
    global rotation_manager

    print(f"""
╔══════════════════════════════════════════════╗
║   🔄  USERNAME ROTATOR                    🔄
║   Prefix: {BOT_PREFIX:<34} ║
║   Owner:  {str(OWNER_ID):<34} ║
╚══════════════════════════════════════════════╝
""")

    log("🚀 Starting...")

    try:
        await app.start()
    except (AuthKeyUnregistered, SessionRevoked, UserDeactivated) as e:
        print(f"❌ Session error: {e}")
        sys.exit(1)

    me = await app.get_me()
    log(f"✅ Logged in as: {me.first_name} (@{me.username})")

    # Load commands
    log("📦 Loading modules...")
    try:
        from modules import commands
        commands.register(app)
        log("✅ Modules loaded")
    except Exception as e:
        log(f"⚠️  Module load failed: {e}")

    # Rotation manager
    log("🔄 Starting rotation engine...")
    from core.rotation_manager import RotationManager
    rotation_manager = RotationManager(app)
    await rotation_manager.start_all()

    # Notify owner
    try:
        await app.send_message(
            OWNER_ID,
            f"🚀 <b>Username Rotator online!</b>\n\n"
            f"👤 {me.mention}\n"
            f"👥 Accounts: <code>{len(rotation_manager.accounts)}</code>\n"
            f"📢 Channels: <code>{len(rotation_manager.tasks)}</code>"
        )
        log("📨 Owner notified")
    except Exception as e:
        log(f"⚠️  Notify failed: {e}")

    log("✅ Ready")


async def shutdown(sig=None):
    global _shutdown_event
    if _shutdown_event is None or _shutdown_event.is_set():
        return
    _shutdown_event.set()

    log("🛑 Shutting down...")
    try:
        if rotation_manager:
            await rotation_manager.stop_all()
        if app and app.is_connected:
            await app.stop()
    except Exception:
        pass


def signal_handler(sig, frame):
    if _shutdown_event is not None:
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(shutdown(sig))
        except Exception:
            pass


async def main():
    global app, _shutdown_event

    _shutdown_event = asyncio.Event()

    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    except Exception:
        pass

    app = create_main_client()
    await startup()
    await _shutdown_event.wait()


if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("accounts").mkdir(exist_ok=True)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("👋 Bye")
