"""
🎮 Premium Control Commands
"""

from pyrogram import filters
from config import BOT_PREFIX, OWNER_ID
from core.colors import C
from core.metrics import metrics
from modules.utils import (
    cmd_filter, format_uptime, humanize_number,
    truncate, split_chunks,
)

import main


PREFIX = BOT_PREFIX


def cmd(name):
    return cmd_filter(name, PREFIX)


def _owner_only(message):
    return message.from_user and message.from_user.id == OWNER_ID


def register(app):

    @app.on_message(cmd("start") | cmd("help"))
    async def start_cmd(client, message):
        p = PREFIX
        text = (
            f"{C.PURPLE}{C.BOLD}🔄 USERNAME ROTATOR{C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"
            f"{C.PINK}📊 STATUS{C.RESET}\n"
            f"  <code>{p}status</code>    — Live dashboard\n"
            f"  <code>{p}metrics</code>   — Detailed stats\n"
            f"  <code>{p}uptime</code>    — Bot uptime\n\n"
            f"{C.PINK}👥 ACCOUNTS{C.RESET}\n"
            f"  <code>{p}accounts</code>  — List all accounts\n"
            f"  <code>{p}channels</code>  — List all channels\n"
            f"  <code>{p}acc &lt;name&gt;</code>  — Account detail\n\n"
            f"{C.PINK}🎮 CONTROL{C.RESET}\n"
            f"  <code>{p}rotate &lt;acc&gt; &lt;ch&gt;</code> — Manual rotate\n"
            f"  <code>{p}reload</code>    — Reload rotations.json\n"
            f"  <code>{p}stop</code>      — Stop all rotations\n"
            f"  <code>{p}restart</code>   — Restart bot\n\n"
            f"{C.PINK}🔐 SECURITY{C.RESET}\n"
            f"  <code>{p}encrypt &lt;s&gt;</code> — Encrypt session\n"
            f"  <code>{p}decrypt &lt;s&gt;</code> — Decrypt session\n\n"
            f"{C.DIM}Built by Sakil 💜{C.RESET}"
        )
        await message.edit(text)

    @app.on_message(cmd("status"))
    async def status_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")
        s = rm.get_status()
        m = metrics.summary()
        text = (
            f"{C.PURPLE}{C.BOLD}📊 LIVE DASHBOARD{C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"
            f"{C.PINK}⏱ UPTIME{C.RESET}\n"
            f"   <code>{m['uptime']}</code>\n\n"
            f"{C.PINK}📈 STATS{C.RESET}\n"
            f"   Accounts:  <code>{m['accounts']}</code>\n"
            f"   Channels:  <code>{m['channels']}</code>\n"
            f"   Rotations: <code>{humanize_number(m['rotations'])}</code>\n"
            f"   Failures:  <code>{m['failures']}</code>\n"
            f"   Success:   <code>{m['success_rate']}</code>\n\n"
            f"{C.PINK}👥 ACTIVE ACCOUNTS{C.RESET}\n"
        )
        if not s:
            text += "   <i>No accounts running</i>\n"
        else:
            for acc, data in s.items():
                text += f"   • <b>{acc}</b> — <code>{data['count']}</code> channels\n"
        top = metrics.top_accounts(3)
        if top:
            text += f"\n{C.PINK}🏆 TOP PERFORMERS{C.RESET}\n"
            for acc, count in top:
                text += f"   • <code>{acc}</code> — {count} rotations\n"
        await message.edit(text)

    @app.on_message(cmd("metrics"))
    async def metrics_cmd(client, message):
        m = metrics.summary()
        text = (
            f"{C.PURPLE}{C.BOLD}📈 DETAILED METRICS{C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"
            f"⏱ Uptime:       <code>{m['uptime']}</code>\n"
            f"🔄 Rotations:    <code>{m['rotations']}</code>\n"
            f"❌ Failures:     <code>{m['failures']}</code>\n"
            f"📊 Success rate: <code>{m['success_rate']}</code>\n"
            f"👥 Accounts:     <code>{m['accounts']}</code>\n"
            f"📢 Channels:     <code>{m['channels']}</code>\n\n"
            f"{C.PINK}🕐 RECENT ACTIVITY{C.RESET}\n"
        )
        if not metrics.recent:
            text += "   <i>No activity yet</i>\n"
        else:
            for r in metrics.recent[-5:]:
                uname = truncate(r.get("username", ""), 20)
                text += f"   {r['status']} <code>{r['account']}</code> → <code>@{uname}</code>\n"
        await message.edit(text)

    @app.on_message(cmd("uptime"))
    async def uptime_cmd(client, message):
        m = metrics.summary()
        await message.edit(
            f"⏱ <b>Uptime:</b> <code>{m['uptime']}</code>\n"
            f"📊 <b>Rotations:</b> <code>{m['rotations']}</code>"
        )

    @app.on_message(cmd("accounts"))
    async def accounts_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Offline")
        accounts = list(rm.accounts.keys())
        if not accounts:
            return await message.edit("📭 No accounts")
        text = (
            f"{C.PURPLE}{C.BOLD}👥 ACCOUNTS ({len(accounts)}){C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"
        )
        for i, acc in enumerate(accounts, 1):
            chans = rm.get_account_channels(acc)
            text += f"   {i}. <b>{acc}</b> — <code>{len(chans)}</code> channels\n"
        await message.edit(text)

    @app.on_message(cmd("channels"))
    async def channels_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Offline")
        tasks = list(rm.tasks.keys())
        if not tasks:
            return await message.edit("📭 No channels")
        text = (
            f"{C.PURPLE}{C.BOLD}📢 CHANNELS ({len(tasks)}){C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"
        )
        for acc, ch in tasks:
            text += f"   • <code>{acc}</code> → <code>{ch}</code>\n"
        await message.edit(text)

    @app.on_message(cmd("acc"))
    async def acc_detail(client, message):
        rm = main.rotation_manager
        args = message.text.split()
        if len(args) < 2:
            return await message.edit("⚠️ <code>.acc sakil1</code>")
        acc_name = args[1]
        if not rm or acc_name not in rm.accounts:
            return await message.edit(f"❌ Account not found: {acc_name}")
        client_obj = rm.accounts[acc_name]
        try:
            me = await client_obj.get_me()
        except Exception as e:
            return await message.edit(f"❌ <code>{e}</code>")
        chans = rm.get_account_channels(acc_name)
        text = (
            f"{C.PURPLE}{C.BOLD}👤 ACCOUNT: {acc_name}{C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"
            f"<b>Name:</b> {me.first_name} {me.last_name or ''}\n"
            f"<b>Username:</b> @{me.username or '—'}\n"
            f"<b>ID:</b> <code>{me.id}</code>\n"
            f"<b>Phone:</b> <code>{me.phone_number or '—'}</code>\n"
            f"<b>Channels:</b> <code>{len(chans)}</code>\n\n"
        )
        for ch in chans:
            text += f"   • <code>{ch}</code>\n"
        await message.edit(text)

    @app.on_message(cmd("rotate"))
    async def manual_rotate(client, message):
        from pyrogram.raw.functions.channels import UpdateUsername
        rm = main.rotation_manager
        if not _owner_only(message):
            return await message.edit("❌ Owner only")
        if not rm:
            return await message.edit("❌ Offline")
        args = message.text.split()
        if len(args) < 3:
            return await message.edit(f"⚠️ <code>{PREFIX}rotate sakil1 -1001234567890</code>")
        acc_name = args[1]
        try:
            ch_id = int(args[2])
        except ValueError:
            return await message.edit("❌ Invalid channel ID")
        if acc_name not in rm.accounts:
            return await message.edit(f"❌ Account: {acc_name}")
        acc_conf = rm.config["accounts"].get(acc_name, {})
        ch_conf = None
        for c in acc_conf.get("channels", []):
            if c["channel_id"] == ch_id:
                ch_conf = c
                break
        if not ch_conf:
            return await message.edit("❌ Channel not in config")
        await message.edit(f"🔄 Rotating {acc_name}/{ch_id}...")
        pool = ch_conf["pool"]
        client_obj = rm.accounts[acc_name]
        key = (acc_name, ch_id)
        idx = rm.indexes.get(key, 0)
        new_username = pool[idx % len(pool)]
        try:
            chat = await client_obj.get_chat(ch_id)
            peer = await client_obj.resolve_peer(chat.id)
            await client_obj.invoke(UpdateUsername(channel=peer, username=new_username))
            rm.indexes[key] = (idx + 1) % len(pool)
            await message.edit(f"✅ Rotated to @{new_username}")
        except Exception as e:
            await message.edit(f"❌ <code>{e}</code>")

    @app.on_message(cmd("reload"))
    async def reload_cmd(client, message):
        rm = main.rotation_manager
        if not _owner_only(message):
            return await message.edit("❌ Owner only")
        if not rm:
            return await message.edit("❌ Offline")
        await message.edit("🔄 Reloading...")
        try:
            await rm.stop_all()
            await rm.start_all()
            await message.edit(
                f"✅ <b>Reloaded!</b>\n\n"
                f"👥 Accounts: <code>{len(rm.accounts)}</code>\n"
                f"📢 Channels: <code>{len(rm.tasks)}</code>"
            )
        except Exception as e:
            await message.edit(f"❌ <code>{e}</code>")

    @app.on_message(cmd("stop"))
    async def stop_cmd(client, message):
        rm = main.rotation_manager
        if not _owner_only(message):
            return await message.edit("❌ Owner only")
        if not rm:
            return await message.edit("❌ Offline")
        await rm.stop_all()
        await message.edit("🛑 <b>All rotations stopped</b>")

    @app.on_message(cmd("restart"))
    async def restart_cmd(client, message):
        import os, sys
        if not _owner_only(message):
            return await message.edit("❌ Owner only")
        await message.edit("♻️ <b>Restarting...</b>")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @app.on_message(cmd("encrypt"))
    async def encrypt_cmd(client, message):
        from core.session_vault import SessionVault
        args = message.text.split(None, 1)
        if len(args) < 2:
            return await message.edit("⚠️ <code>.encrypt session_string</code>")
        try:
            locked = SessionVault().lock(args[1].strip())
            await message.edit(f"🔐 <b>Encrypted:</b>\n<code>{locked}</code>")
        except Exception as e:
            await message.edit(f"❌ <code>{e}</code>")

    @app.on_message(cmd("decrypt"))
    async def decrypt_cmd(client, message):
        from core.session_vault import SessionVault
        if not _owner_only(message):
            return await message.edit("❌ Owner only")
        args = message.text.split(None, 1)
        if len(args) < 2:
            return await message.edit("⚠️ <code>.decrypt encrypted_string</code>")
        try:
            plain = SessionVault().unlock(args[1].strip())
            await message.edit(f"🔓 <b>Decrypted:</b>\n<code>{plain}</code>")
        except Exception as e:
            await message.edit(f"❌ <code>{e}</code>")

    @app.on_message(cmd("ping"))
    async def ping_cmd(client, message):
        import time
        t1 = time.time()
        msg = await message.edit("🏓 Pong...")
        t2 = time.time()
        latency = (t2 - t1) * 1000
        m = metrics.summary()
        await msg.edit(
            f"🏓 <b>Pong!</b>\n\n"
            f"⚡ <b>Latency:</b> <code>{latency:.2f}ms</code>\n"
            f"⏱ <b>Uptime:</b> <code>{m['uptime']}</code>\n"
            f"🔄 <b>Rotations:</b> <code>{m['rotations']}</code>"
        )
