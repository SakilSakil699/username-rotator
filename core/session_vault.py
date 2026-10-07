"""
🔐 Session Vault — AES-128 Fernet Encryption
Stolen sessions useless banata hai
"""

import os
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken


class SessionVaultError(Exception):
    """Vault-specific errors."""
    pass


class SessionVault:
    """Encrypt/decrypt session strings."""

    TOKEN_PREFIX = "gAAAAA"

    def __init__(self, master_key=None):
        if master_key is None:
            try:
                from config import VAULT_KEY
                master_key = VAULT_KEY
            except Exception:
                master_key = os.getenv("VAULT_KEY", "")

        if not master_key:
            raise SessionVaultError(
                "VAULT_KEY missing!\n"
                "Add to .env: VAULT_KEY=your-32-char-random-key"
            )

        if len(master_key) < 16:
            raise SessionVaultError(
                "VAULT_KEY too short! Use 32+ characters."
            )

        self._master = master_key
        self._fernet = self._build_fernet(master_key)

    @staticmethod
    def _build_fernet(master_key):
        """Derive Fernet key from master key via SHA256."""
        digest = hashlib.sha256(master_key.encode("utf-8")).digest()
        key = base64.urlsafe_b64encode(digest)
        return Fernet(key)

    def lock(self, plain):
        """Encrypt session string."""
        if not plain:
            raise SessionVaultError("Empty session.")
        if self.is_locked(plain):
            return plain

        try:
            return self._fernet.encrypt(plain.encode("utf-8")).decode("utf-8")
        except Exception as e:
            raise SessionVaultError(f"Encryption failed: {e}")

    def unlock(self, encrypted):
        """Decrypt session string."""
        if not encrypted:
            raise SessionVaultError("Empty session.")

        if not self.is_locked(encrypted):
            return encrypted

        try:
            return self._fernet.decrypt(
                encrypted.encode("utf-8")
            ).decode("utf-8")
        except InvalidToken:
            raise SessionVaultError(
                "Invalid token! Either:\n"
                "  1. Wrong VAULT_KEY\n"
                "  2. Session tampered\n"
                "  3. Different machine encrypted it"
            )
        except Exception as e:
            raise SessionVaultError(f"Decryption failed: {e}")

    @classmethod
    def is_locked(cls, value):
        """Check if string is a Fernet token."""
        return bool(value) and value.startswith(cls.TOKEN_PREFIX)

    @classmethod
    def auto_unlock(cls, value):
        """Auto-detect and decrypt."""
        if not value:
            return value
        if not cls.is_locked(value):
            return value
        return cls().unlock(value)


# ═══════════════════════════════════════════
#  CLI Test
# ═══════════════════════════════════════════
if __name__ == "__main__":
    import sys

    print("═" * 60)
    print("🔐 Session Vault — Test")
    print("═" * 60)

    try:
        vault = SessionVault()
    except SessionVaultError as e:
        print(f"❌ {e}")
        print("\n👉 Generate key:")
        print("   python -c \"import base64,os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())\"")
        sys.exit(1)

    test = "BQACAgUAAxkBAAIC_TEST_SESSION_1234"
    print(f"\n📝 Original : {test}")

    locked = vault.lock(test)
    print(f"🔐 Locked   : {locked[:40]}...")

    unlocked = vault.unlock(locked)
    print(f"🔓 Unlocked : {unlocked}")

    if unlocked == test:
        print("\n✅ SUCCESS — Vault working!")
    else:
        print("\n❌ FAILED")
        sys.exit(1)
