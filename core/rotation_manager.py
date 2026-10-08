"""
🔄 Rotation Manager — Simple Per-Account Control
Commands: .start .stop .on <acc> .off <acc>
"""

import asyncio
import json
import os
import time
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
    def __init__(self, main_app):
        self.main_app = main_app
        self.accounts = {}       # {name: Client}
        self.tasks = {}          # {(acc, ch): Task}
        self.indexes = {}        # {(acc, ch): int}
        self.config = {}
        self.chat_cache = {}
        self.start_time = time.time()

    # ═════════════════════════════════════
    #  CONFIG
    # ═════════════════════════════════════
    def load_config(self):
        if not CONFIG_FILE.exists():
            log.warning("rotations.json not found")
            self.config = {"accounts": {}}
            return
        with open(CONFIG_FILE, encoding="utf-8") as f:
            self.config = json.load(f)
        count = len(self.config.get("accounts", {}))
        log.info(f"Loaded config: {C.PINK}{count}{C.RESET} accounts")

    # ═════════════════════════════════════
    #  LOGIN ALL (idle)
    # ═════════════════════════════════════
    async def load_accounts(self):
        self.load_config()
        accounts = self.config.get("accounts", {})
        if not accounts:
            log.warning("No accounts configured")
            return
        for acc_name, acc_data in accounts.items():
            try:
                await self._login_account(acc_name, acc_data)
            except Exception as e:
                log.error(f"{acc_name}: {e}")
        log.info(f"✅ Logged in {C.PINK}{len(self.accounts)}{C.RESET} accounts (IDLE)")

    async def _login_account(self, acc_name, acc_data):
        from config import API_ID, API_HASH
        session_string = os.getenv(f"SESSION_{acc_name.upper()}")
        session_file = SESSIONS_DIR / f"{acc_name}.session"
        client = None

        if session_string:
            if session_string.startswith("gAAAAA"):
                try:
                    from core.session_vault import SessionVault
                    session_string = SessionVault().unlock(session_string)
                except Exception as e:
                    log.error(f"{acc_name} decrypt failed: {e}")
                    return
            client = Client(
                name=f"acc_{acc_name}",
                api_id=API_ID, api_hash=API_HASH,
                session_string=session_string, in_memory=True,
            )
        elif session_file.exists():
            try:
                content = session_file.read_text().strip()
            except Exception as e:
                log.error(f"{acc_name} read failed: {e}")
                return
            if content.startswith("gAAAAA") or content.startswith("BQACAg"):
                if content.startswith("gAAAAA"):
                    try:
                        from core.session_vault import SessionVault
                        content = SessionVault().unlock(content)
                    except Exception as e:
                        log.error(f"{acc_name} decrypt failed: {e}")
                        return
                client = Client(
                    name=f"acc_{acc_name}",
                    api_id=API_ID, api_hash=API_HASH,
                    session_string=content, in_memory=True,
                )
            else:
                client = Client(
                    name=str(session_file.with_suffix("")),
                    api_id=API_ID, api_hash=API_HASH,
                )
        else:
            log.error(f"No session for {acc_name}")
            return

        await client.start()
        me = await client.get_me()
        log.info(f"{C.PINK}{acc_name}{C.RESET} → {me.first_name} (@{me.username})")
        self.accounts[acc_name] = client
        await self._cache_chats(acc_name, client, acc_data)

    async def _cache_chats(self, acc_name, client, acc_data):
        needed_ids = set()
        for ch_conf in acc_data.get("channels", []):
            if ch_conf.get("enabled", True):
                needed_ids.add(ch_conf["channel_id"])
        if not needed_ids:
            return
        cached = 0
        try:
            async for dialog in client.get_dialogs():
                chat = dialog.chat
                if chat.id in needed_ids:
                    self.chat_cache[(acc_name, chat.id)] = chat
                    cached += 1
                    if cached >= len(needed_ids):
                        break
        except Exception as e:
            log.warning(f"Cache error {acc_name}: {e}")

    # ═════════════════════════════════════
    #  START / STOP — SINGLE ACCOUNT
    # ═════════════════════════════════════
    async def start_account(self, acc_name):
        """Start rotation for ONE account."""
        if acc_name not in self.accounts:
            return False, f"Account '{acc_name}' not loaded"

        acc_data = self.config.get("accounts", {}).get(acc_name, {})
        started = 0

        for ch_conf in acc_data.get("channels", []):
            if not ch_conf.get("enabled", True):
                continue
            ch_id = ch_conf["channel_id"]
            key = (acc_name, ch_id)

            # Already running? Skip
            if key in self.tasks and not self.tasks[key].done():
                continue

            task = asyncio.create_task(
                self._rotation_loop(acc_name, self.accounts[acc_name], ch_conf)
            )
            self.tasks[key] = task
            started += 1

        if started == 0:
            return False, f"No new channels for {acc_name}"

        log.info(f"▶️  {C.PINK}{acc_name}{C.RESET} started ({started} channels)")
        return True, f"Started {started} channels for {acc_name}"

    async def stop_account(self, acc_name):
        """Stop rotation for ONE account."""
        keys = [(a, ch) for (a, ch) in self.tasks.keys() if a == acc_name]

        if not keys:
            return False, f"No active rotations for {acc_name}"

        for key in keys:
            self.tasks[key].cancel()
            del self.tasks[key]

        log.info(f"⏸  {C.PINK}{acc_name}{C.RESET} stopped ({len(keys)} channels)")
        return True, f"Stopped {len(keys)} channels for {acc_name}"

    # ═════════════════════════════════════
    #  START / STOP — ALL ACCOUNTS
    # ═════════════════════════════════════
    async def start_all_accounts(self):
        """Start ALL accounts."""
        total = 0
        for acc_name in self.accounts.keys():
            ok, _ = await self.start_account(acc_name)
            if ok:
                total += 1
        return total

    async def stop_all_accounts(self):
        """Stop ALL accounts."""
        total = 0
        for acc_name in list(self.accounts.keys()):
            ok, _ = await self.stop_account(acc_name)
            if ok:
                total += 1
        return total

    # ═════════════════════════════════════
    #  ROTATION LOOP
    # ═════════════════════════════════════
    async def _rotation_loop(self, acc_name, client, conf):
        ch_id = conf["channel_id"]
        interval = conf.get("interval", 1800)
        pool = conf.get("pool", [])
        if not pool:
            return
        key = (acc_name, ch_id)
        if key not in self.indexes:
            self.indexes[key] = 0
        await asyncio.sleep(10)

        while True:
            try:
                target_chat = self.chat_cache.get((acc_name, ch_id))
                if not target_chat:
                    async for dialog in client.get_dialogs():
                        if dialog.chat.id == ch_id:
                            target_chat = dialog.chat
                            self.chat_cache[(acc_name, ch_id)] = target_chat
                            break
                if not target_chat:
                    raise Exception(f"Channel not accessible: {ch_id}")

                try:
                    fresh = await client.get_chat(target_chat.id)
                    current = fresh.username
                except Exception:
                    current = target_chat.username

                idx = self.indexes[key]
                new_username = None
                for i in range(len(pool)):
                    candidate = pool[(idx + i) % len(pool)]
                    if candidate != current:
                        new_username = candidate
                        self.indexes[key] = (idx + i + 1) % len(pool)
                        break

                if not new_username:
                    await asyncio.sleep(interval)
                    continue

                peer = await client.resolve_peer(target_chat.id)
                try:
                    await client.invoke(UpdateUsername(channel=peer, username=new_username))
                except Exception as ue:
                    err = str(ue)
                    if "USERNAME_NOT_MODIFIED" in err:
                        target_chat.username = new_username
                        await asyncio.sleep(interval)
                        continue
                    if "USERNAME_OCCUPIED" in err:
                        await asyncio.sleep(interval)
                        continue
                    if "FLOOD_WAIT" in err:
                        import re
                        m = re.search(r"FLOOD_WAIT_(\d+)", err)
                        wait = int(m.group(1)) if m else 60
                        log.warning(f"{acc_name}/{ch_id}: flood {wait}s")
                        await asyncio.sleep(wait + 5)
                        continue
                    raise

                target_chat.username = new_username
                metrics.record_success(acc_name, ch_id, new_username)
                log.info(f"{C.PURPLE}{acc_name}{C.RESET} {C.DIM}→{C.RESET} {C.PINK}@{new_username}{C.RESET}")

                await self._notify_owner(
                    f"✅ <b>Rotated</b>\n\n"
                    f"👤 <code>{acc_name}</code>\n"
                    f"📢 <code>{ch_id}</code>\n"
                    f"🔗 @{new_username}"
                )
            except asyncio.CancelledError:
                return
            except Exception as e:
                metrics.record_failure(acc_name, ch_id, e)
                log.error(f"{acc_name}/{ch_id}: {e}")
            await asyncio.sleep(interval)

    async def _notify_owner(self, text):
        try:
            from config import OWNER_ID
            await self.main_app.send_message(OWNER_ID, text)
        except Exception:
            pass

    # ═════════════════════════════════════
    #  MANUAL ROTATE
    # ═════════════════════════════════════
    async def rotate_once(self, acc_name, ch_id):
        if acc_name not in self.accounts:
            return False, f"Account '{acc_name}' not loaded"

        acc_data = self.config.get("accounts", {}).get(acc_name, {})
        ch_conf = None
        for c in acc_data.get("channels", []):
            if c["channel_id"] == ch_id:
                ch_conf = c
                break

        if not ch_conf:
            return False, f"Channel {ch_id} not in config for {acc_name}"

        pool = ch_conf.get("pool", [])
        if not pool:
            return False, "Empty pool"

        client = self.accounts[acc_name]
        key = (acc_name, ch_id)
        idx = self.indexes.get(key, 0)
        new_username = pool[idx % len(pool)]

        try:
            chat = await client.get_chat(ch_id)
            peer = await client.resolve_peer(chat.id)
            await client.invoke(UpdateUsername(channel=peer, username=new_username))
            self.indexes[key] = (idx + 1) % len(pool)
            return True, new_username
        except Exception as e:
            return False, str(e)

    # ═════════════════════════════════════
    #  STATUS
    # ═════════════════════════════════════
    def get_status(self):
        s = {}
        for acc_name in self.accounts.keys():
            channels = [ch for (a, ch) in self.tasks.keys() if a == acc_name]
            s[acc_name] = {"channels": channels, "count": len(channels)}
        return s

    def is_account_running(self, acc_name):
        return any(a == acc_name for (a, ch) in self.tasks.keys())

    def get_running_accounts(self):
        return list(set(a for (a, ch) in self.tasks.keys()))

    def get_global_status(self):
        return {
            "accounts_loaded": len(self.accounts),
            "total_accounts": len(self.config.get("accounts", {})),
            "active_channels": len(self.tasks),
            "running_accounts": self.get_running_accounts(),
        }

    async def shutdown_all(self):
        await self.stop_all_accounts()
        for client in self.accounts.values():
            try:
                await client.stop()
            except Exception:
                pass
        self.accounts.clear()
        self.chat_cache.clear()
