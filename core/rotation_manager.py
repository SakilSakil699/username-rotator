"""
🔄 Rotation Manager — Multi-Account Engine
Fixes: Peer id invalid + USERNAME_NOT_MODIFIED
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
    def __init__(self, main_app):
        self.main_app = main_app
        self.accounts = {}
        self.tasks = {}
        self.indexes = {}
        self.config = {}
        self.chat_cache = {}

    def load_config(self):
        if not CONFIG_FILE.exists():
            log.warning("rotations.json not found")
            self.config = {"accounts": {}}
            return
        with open(CONFIG_FILE, encoding="utf-8") as f:
            self.config = json.load(f)
        count = len(self.config.get("accounts", {}))
        log.info(f"Loaded config: {C.PINK}{count}{C.RESET} accounts")

    async def start_all(self):
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

    async def _start_account(self, acc_name, acc_data):
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

        for ch_conf in acc_data.get("channels", []):
            if not ch_conf.get("enabled", True):
                continue
            ch_id = ch_conf["channel_id"]
            task = asyncio.create_task(self._rotation_loop(acc_name, client, ch_conf))
            self.tasks[(acc_name, ch_id)] = task

    async def _cache_chats(self, acc_name, client, acc_data):
        needed_ids = set()
        for ch_conf in acc_data.get("channels", []):
            if ch_conf.get("enabled", True):
                needed_ids.add(ch_conf["channel_id"])
        if not needed_ids:
            return
        log.info(f"Caching chats for {acc_name}...")
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
        found = len([(a, c) for (a, c) in self.chat_cache.keys() if a == acc_name])
        log.info(f"Cached {C.PINK}{found}{C.RESET}/{len(needed_ids)} channels for {acc_name}")

    async def _rotation_loop(self, acc_name, client, conf):
        ch_id = conf["channel_id"]
        interval = conf.get("interval", 1800)
        pool = conf.get("pool", [])
        if not pool:
            log.warning(f"{acc_name}/{ch_id}: empty pool")
            return
        key = (acc_name, ch_id)
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
                    log.warning(f"{acc_name}/{ch_id}: all pool usernames == current")
                    await asyncio.sleep(interval)
                    continue

                peer = await client.resolve_peer(target_chat.id)
                try:
                    await client.invoke(UpdateUsername(channel=peer, username=new_username))
                except Exception as ue:
                    err = str(ue)
                    if "USERNAME_NOT_MODIFIED" in err:
                        log.warning(f"{acc_name}/{ch_id}: unchanged, moving on")
                        target_chat.username = new_username
                        await asyncio.sleep(interval)
                        continue
                    if "USERNAME_OCCUPIED" in err:
                        log.warning(f"{acc_name}/{ch_id}: @{new_username} occupied")
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

    async def _notify_owner(self, text):
        try:
            from config import OWNER_ID
            await self.main_app.send_message(OWNER_ID, text)
        except Exception:
            pass

    async def stop_all(self):
        for task in self.tasks.values():
            task.cancel()
        self.tasks.clear()
        for client in self.accounts.values():
            try:
                await client.stop()
            except Exception:
                pass
        self.accounts.clear()
        self.chat_cache.clear()
        log.info("All stopped")

    def get_status(self):
        s = {}
        for acc_name in self.accounts.keys():
            channels = [ch for (a, ch) in self.tasks.keys() if a == acc_name]
            s[acc_name] = {"channels": channels, "count": len(channels)}
        return s

    def get_account_channels(self, acc_name):
        return [ch for (a, ch) in self.tasks.keys() if a == acc_name]
