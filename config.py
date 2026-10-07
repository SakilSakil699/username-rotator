"""
⚙️  Config Loader
Premium Username Rotator
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ═══════════════════════════════════════════
#  🔑 TELEGRAM
# ═══════════════════════════════════════════
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))


# ═══════════════════════════════════════════
#  🔐 SECURITY
# ═══════════════════════════════════════════
VAULT_KEY = os.getenv("VAULT_KEY", "")


# ═══════════════════════════════════════════
#  🤖 BOT
# ═══════════════════════════════════════════
BOT_NAME = "Username Rotator"
BOT_PREFIX = "."


# ═══════════════════════════════════════════
#  ✅ VALIDATION
# ═══════════════════════════════════════════
def validate():
    missing = []
    if not API_ID: missing.append("API_ID")
    if not API_HASH: missing.append("API_HASH")
    if not SESSION_STRING: missing.append("SESSION_STRING")
    if not OWNER_ID: missing.append("OWNER_ID")

    if missing:
        print("⚠️  Missing in .env:")
        for m in missing:
            print(f"   • {m}")
        return False
    return True


if __name__ != "__main__":
    validate()
