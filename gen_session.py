"""
🔑 Session Generator
Multi-account ke liye
"""

import asyncio

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import sys
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import (
    PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired,
    SessionPasswordNeeded, PasswordHashInvalid,
)

from config import API_ID, API_HASH, VAULT_KEY


def banner():
    print("""
╔══════════════════════════════════════════════╗
║      🔑 SESSION GENERATOR 🔑                 ║
╚══════════════════════════════════════════════╝
""")


async def generate():
    banner()

    if not API_ID or not API_HASH:
        print("❌ API_ID/API_HASH missing in .env")
        sys.exit(1)

    app = Client(":memory:", api_id=API_ID, api_hash=API_HASH, in_memory=True)

    async with app:
        phone = input("📞 Phone (+country code): ").strip()
        if not phone.startswith("+"):
            phone = "+" + phone

        sent = await app.send_code(phone)
        print(f"✅ OTP sent to {phone}")

        code = input("🔢 OTP: ").strip().replace(" ", "")

        try:
            signed = await app.sign_in(phone, sent.phone_code_hash, code)
        except SessionPasswordNeeded:
            pwd = input("🔒 2FA Password: ").strip()
            signed = await app.check_password(pwd)

        session = await app.export_session_string()
        me = signed

        print("\n" + "═" * 50)
        print(f"✅ LOGIN SUCCESSFUL")
        print(f"👤 {me.first_name} (@{me.username})")
        print(f"🆔 {me.id}")
        print("═" * 50)

        if VAULT_KEY:
            try:
                from core.session_vault import SessionVault
                session = SessionVault().lock(session)
                print("🔐 Encrypted with VAULT_KEY")
            except Exception:
                pass

        print(f"\n🔑 SESSION:\n{session}\n")

        # Save
        name = input("💾 Save as (e.g. sakil1): ").strip()
        if name:
            Path("sessions").mkdir(exist_ok=True)
            f = Path("sessions") / f"{name}.session"
            f.write_text(session)
            print(f"✅ Saved: {f}")


if __name__ == "__main__":
    try:
        asyncio.run(generate())
    except KeyboardInterrupt:
        print("\n⚠️ Cancelled")
