"""
🔄 Rotation Manager — Multi-Account Engine
Har account + channel ka apna independent loop
"""

import asyncio
import json
import os
from pathlib import Path
from pyrogram import Client
from pyrogram.raw.functions.channels import UpdateUsername

from core.logger import log
from core.metrics import metrics
from core.colors import C


CONFIG_FILE = Path("rotations.json")
SESSIONS_DIR = Path("accounts")
SESSIONS_DIR.mkdir(exist_ok=True)


class RotationManager:
    """Multi-account username rotation engine."""

    def __init__(self, main_app):
        self.main_app = main_app
        self.accounts = {}
        self.tasks = {}
        self.indexes = {}
        self.config = {}

    # ═════════════════════════════════════
    #  CONFIG
    # ═════════════════════════════════════
    def load_config(self):
        """Load rotations.json."""
        if not CONFIG_FILE.exists():
            log.warning("rotations.json not found")
            self.config = {"accounts": {}}
            return

        with open(CONFIG_FILE, encoding="utf-8") as f:
            self.config = json.load(f)

        count = len(self.config.get("accounts", {}))
        log.info(f"Loaded config: {C.PINK}{count}{C.RESET} accounts")

    # ═════════════════════════════════════
    #  START ALL
    # ═════════════════════════════════════
    async def start_all(self):
        """Start all accounts from config."""
        self.load_config()

        accounts = self.config.get("accounts", {})
        if not accounts:
            log.warning("No accounts configured")
            return

        for acc_name, acc_data in accounts.items():
            try:
                await self._start_account(acc_name, acc_data)
            except Exception as e:
                log.error(f"{acc_name}: {e}")
                await self._notify_owner(
                    f"❌ <b>Account failed:</b> {acc_name}\n<code>{e}</code>"
                )

        log.info(
            f"Started {C.PINK}{len(self.accounts)}{C.RESET} accounts, "
            f"{C.PINK}{len(self.tasks)}{C.RESET} channels"
        )

    # ═════════════════════════════════════
    #  START ONE ACCOUNT (Smart Session Detection)
    # ═════════════════════════════════════
    async def _start_account(self, acc_name, acc_data):
        """Start a single account with smart session detection."""
        from config import API_ID, API_HASH

        session_string = os.getenv(f"SESSION_{acc_name.upper()}")
        session_file = SESSIONS_DIR / f"{acc_name}.session"

        client = None

        # ─────────────────────────────────
        #  Priority 1: .env SESSION_<NAME>
        # ─────────────────────────────────
        if session_string:
            log.info(f"{acc_name}: using .env session")

            # Decrypt if vaulted
            if session_string.startswith("gAAAAA"):
                try:
                    from core.session_vault import SessionVault
                    session_string = SessionVault().unlock(session_string)
                except Exception as e:
                    log.error(f"{acc_name} decrypt failed: {e}")
                    return

            client = Client(
                name=f"acc_{acc_name}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=session_string,
                in_memory=True,
            )

        # ─────────────────────────────────
        #  Priority 2: accounts/<name>.session file
        # ─────────────────────────────────
        elif session_file.exists():
            log.info(f"{acc_name}: using file session")

            try:
                content = session_file.read_text().strip()
            except Exception as e:
                log.error(f"{acc_name} read failed: {e}")
                return

            # Detect type: string session or SQLite file
            if content.startswith("gAAAAA") or content.startswith("BQACAg"):
                # String session (encrypted or plain)
                if content.startswith("gAAAAA"):
                    try:
                        from core.session_vault import SessionVault
                        content = SessionVault().unlock(content)
                    except Exception as e:
                        log.error(f"{acc_name} decrypt failed: {e}")
                        return

                client = Client(
                    name=f"acc_{acc_name}",
                    api_id=API_ID,
                    api_hash=API_HASH,
                    session_string=content,
                    in_memory=True,
                )
            else:
                # SQLite file session
                client = Client(
                    name=str(session_file.with_suffix("")),
                    api_id=API_ID,
                    api_hash=API_HASH,
                )

        else:
            log.error(f"No session for {acc_name}")
            return

        # ─────────────────────────────────
        #  Start client
        # ─────────────────────────────────
        await client.start()
        me = await client.get_me()
        log.info(
            f"{C.PINK}{acc_name}{C.RESET} → "
            f"{me.first_name} (@{me.username})"
        )
        self.accounts[acc_name] = client

        # ─────────────────────────────────
        #  Start channel rotation loops
        # ─────────────────────────────────
        for ch_conf in acc_data.get("channels", []):
            if not ch_conf.get("enabled", True):
                continue

            ch_id = ch_conf["channel_id"]
            task = asyncio.create_task(
                self._rotation_loop(acc_name, client, ch_conf)
            )
            self.tasks[(acc_name, ch_id)] = task

    # ═════════════════════════════════════
    #  ROTATION LOOP
    # ═════════════════════════════════════
    async def _rotation_loop(self, acc_name, client, conf):
        """Rotation loop for one channel."""
        ch_id = conf["channel_id"]
        interval = conf.get("interval", 1800)
        pool = conf.get("pool", [])

        if not pool:
            log.warning(f"{acc_name}/{ch_id}: empty pool")
            return

        key = (acc_name, ch_id)
        self.indexes[key] = 0

        # Initial delay (avoid flood on startup)
        await asyncio.sleep(10)

        while True:
            try:
                # ── Get current username ──
                try:
                    chat = await client.get_chat(ch_id)
                    current = chat.username
                except Exception:
                    current = None

                # ── Pick next username ──
                idx = self.indexes[key]
                new_username = pool[idx % len(pool)]

                # Skip if same as current
                if new_username == current:
                    self.indexes[key] = (idx + 1) % len(pool)
                    new_username = pool[self.indexes[key]]

                # ── Change username ──
                chat = await client.get_chat(ch_id)
                peer = await client.resolve_peer(chat.id)

                await client.invoke(
                    UpdateUsername(channel=peer, username=new_username)
                )

                self.indexes[key] = (self.indexes[key] + 1) % len(pool)

                # ── Metrics ──
                metrics.record_success(acc_name, ch_id, new_username)

                log.info(
                    f"{C.PURPLE}{acc_name}{C.RESET} "
                    f"{C.DIM}→{C.RESET} "
                    f"{C.PINK}@{new_username}{C.RESET}"
                )

                # ── Notify owner ──
                await self._notify_owner(
                    f"✅ <b>Rotated</b>\n\n"
                    f"👤 <code>{acc_name}</code>\n"
                    f"📢 <code>{ch_id}</code>\n"
                    f"🔗 @{new_username}"
                )

            except Exception as e:
                metrics.record_failure(acc_name, ch_id, e)
                log.error(f"{acc_name}/{ch_id}: {e}")

                await self._notify_owner(
                    f"❌ <b>Rotation failed</b>\n\n"
                    f"👤 {acc_name}\n"
                    f"📢 {ch_id}\n"
                    f"<code>{str(e)[:200]}</code>"
                )

            await asyncio.sleep(interval)

    # ═════════════════════════════════════
    #  HELPERS
    # ═════════════════════════════════════
    async def _notify_owner(self, text):
        """Send message to owner."""
        try:
            from config import OWNER_ID
            await self.main_app.send_message(OWNER_ID, text)
        except Exception:
            pass

    # ═════════════════════════════════════
    #  STOP
    # ═════════════════════════════════════
    async def stop_all(self):
        """Stop all rotations."""
        for task in self.tasks.values():
            task.cancel()
        self.tasks.clear()

        for client in self.accounts.values():
            try:
                await client.stop()
            except Exception:
                pass
        self.accounts.clear()
        log.info("All stopped")

    # ═════════════════════════════════════
    #  STATUS
    # ═════════════════════════════════════
    def get_status(self):
        """Get status dict."""
        s = {}
        for acc_name in self.accounts.keys():
            channels = [
                ch for (a, ch) in self.tasks.keys() if a == acc_name
            ]
            s[acc_name] = {
                "channels": channels,
                "count": len(channels),
            }
        return s

    def get_account_channels(self, acc_name):
        """Get channels for one account."""
        return [
            ch for (a, ch) in self.tasks.keys() if a == acc_name
        ]
