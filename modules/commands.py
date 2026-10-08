"""
🎮 Simple Control Commands
.start .stop .on .off .list .status .rotate
"""

from pyrogram import filters
from config import BOT_PREFIX, OWNER_ID
from core.colors import C
from core.metrics import metrics

import main


PREFIX = BOT_PREFIX


def cmd(name):
    return filters.command(name, prefixes=PREFIX) & filters.me


def _owner_only(message):
    return message.from_user and message.from_user.id == OWNER_ID


def register(app):

    # ═══════════════════════════════════════════
    #  .start — Start ALL accounts
    # ═══════════════════════════════════════════
    @app.on_message(cmd("start"))
    async def start_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        await message.edit("▶️ Starting all accounts...")

        count = await rm.start_all_accounts()

        await message.edit(
            f"▶️ <b>All accounts started</b>\n\n"
            f"✅ Active: <code>{count}</code> accounts\n"
            f"📢 Channels: <code>{len(rm.tasks)}</code>"
        )

    # ═══════════════════════════════════════════
    #  .stop — Stop ALL accounts
    # ═══════════════════════════════════════════
    @app.on_message(cmd("stop"))
    async def stop_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        await message.edit("⏸ Stopping all accounts...")

        count = await rm.stop_all_accounts()

        await message.edit(
            f"⏸ <b>All accounts stopped</b>\n\n"
            f"✅ Stopped: <code>{count}</code> accounts\n"
            f"📢 Active channels: <code>0</code>"
        )

    # ═══════════════════════════════════════════
    #  .on <acc> [acc2] [acc3]... — Start specific
    # ═══════════════════════════════════════════
    @app.on_message(cmd("on"))
    async def on_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        args = message.text.split()[1:]  # All accounts after .on
        if not args:
            return await message.edit(
                f"⚠️ Usage:\n"
                f"<code>.on sakil1</code>\n"
                f"<code>.on sakil1 sakil2 sakil3</code>"
            )

        await message.edit(f"▶️ Starting {len(args)} account(s)...")

        results = []
        for acc in args:
            ok, msg = await rm.start_account(acc)
            icon = "✅" if ok else "❌"
            results.append(f"{icon} <code>{acc}</code> — {msg}")

        await message.edit(
            f"▶️ <b>Account(s) started</b>\n\n" + "\n".join(results)
        )

    # ═══════════════════════════════════════════
    #  .off <acc> [acc2]... — Stop specific
    # ═══════════════════════════════════════════
    @app.on_message(cmd("off"))
    async def off_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        args = message.text.split()[1:]
        if not args:
            return await message.edit(
                f"⚠️ Usage:\n"
                f"<code>.off sakil1</code>\n"
                f"<code>.off sakil1 sakil2</code>"
            )

        await message.edit(f"⏸ Stopping {len(args)} account(s)...")

        results = []
        for acc in args:
            ok, msg = await rm.stop_account(acc)
            icon = "✅" if ok else "❌"
            results.append(f"{icon} <code>{acc}</code> — {msg}")

        await message.edit(
            f"⏸ <b>Account(s) stopped</b>\n\n" + "\n".join(results)
        )

    # ═══════════════════════════════════════════
    #  .list — List all accounts with status
    # ═══════════════════════════════════════════
    @app.on_message(cmd("list"))
    async def list_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        text = f"{C.PURPLE}{C.BOLD}👥 ALL ACCOUNTS{C.RESET}\n"
        text += f"{C.DIM}{'─' * 42}{C.RESET}\n\n"

        if not rm.accounts:
            return await message.edit(text + "<i>No accounts loaded</i>")

        for acc in rm.accounts.keys():
            is_running = rm.is_account_running(acc)
            chans = rm.get_status().get(acc, {}).get("count", 0)
            status = "🟢 ON " if is_running else "⚫ OFF"
            text += (
                f"{status} <b>{acc}</b> "
                f"— {chans} channels\n"
            )

        text += f"\n{C.DIM}Use .on &lt;acc&gt; / .off &lt;acc&gt;{C.RESET}"

        await message.edit(text)

    # ═══════════════════════════════════════════
    #  .status — Global status
    # ═══════════════════════════════════════════
    @app.on_message(cmd("status"))
    async def status_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        gs = rm.get_global_status()
        m = metrics.summary()

        text = (
            f"{C.PURPLE}{C.BOLD}📊 GLOBAL STATUS{C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"

            f"👥 <b>Accounts:</b>  <code>{gs['accounts_loaded']}/{gs['total_accounts']}</code>\n"
            f"📢 <b>Channels:</b>  <code>{gs['active_channels']}</code>\n"
            f"🟢 <b>Running:</b>   <code>{len(gs['running_accounts'])}</code>\n\n"

            f"{C.PINK}📈 METRICS{C.RESET}\n"
            f"   🔄 Rotations: <code>{m['rotations']}</code>\n"
            f"   ❌ Failures:  <code>{m['failures']}</code>\n"
            f"   ✅ Success:   <code>{m['success_rate']}</code>\n"
            f"   ⏱ Uptime:    <code>{m['uptime']}</code>\n"
        )

        if gs["running_accounts"]:
            text += f"\n{C.PINK}🟢 ACTIVE{C.RESET}\n"
            for acc in gs["running_accounts"]:
                text += f"   • <code>{acc}</code>\n"

        await message.edit(text)

    # ═══════════════════════════════════════════
    #  .rotate <acc> <ch_id> — Manual rotate
    # ═══════════════════════════════════════════
    @app.on_message(cmd("rotate"))
    async def rotate_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")

        args = message.text.split()
        if len(args) < 3:
            return await message.edit(
                f"⚠️ Usage: <code>.rotate sakil1 -1001234567890</code>"
            )

        acc_name = args[1]
        try:
            ch_id = int(args[2])
        except ValueError:
            return await message.edit("❌ Invalid channel ID")

        await message.edit(f"🔄 Rotating {acc_name} / {ch_id}...")

        ok, result = await rm.rotate_once(acc_name, ch_id)

        if ok:
            await message.edit(f"✅ <b>Rotated to @{result}</b>")
        else:
            await message.edit(f"❌ <b>Failed:</b>\n<code>{result}</code>")

    # ═══════════════════════════════════════════
    #  .reload — Reload config
    # ═══════════════════════════════════════════
    @app.on_message(cmd("reload"))
    async def reload_cmd(client, message):
        rm = main.rotation_manager
        if not rm:
            return await message.edit("❌ Manager offline")
        if not _owner_only(message):
            return await message.edit("❌ Owner only")

        await message.edit("🔄 Reloading...")

        # Remember which accounts were running
        running = rm.get_running_accounts()

        await rm.shutdown_all()
        await rm.load_accounts()

        # Restart previously running
        restarted = 0
        for acc in running:
            ok, _ = await rm.start_account(acc)
            if ok:
                restarted += 1

        await message.edit(
            f"✅ <b>Reloaded!</b>\n\n"
            f"👥 Accounts: <code>{len(rm.accounts)}</code>\n"
            f"🟢 Restarted: <code>{restarted}</code>"
        )

    # ═══════════════════════════════════════════
    #  .help — Commands list
    # ═══════════════════════════════════════════
    @app.on_message(cmd("help") | cmd("ping"))
    async def help_cmd(client, message):
        p = PREFIX
        text = (
            f"{C.PURPLE}{C.BOLD}🎮 COMMANDS{C.RESET}\n"
            f"{C.DIM}{'─' * 42}{C.RESET}\n\n"

            f"{C.PINK}🌐 GLOBAL{C.RESET}\n"
            f"  <code>{p}start</code>     — Start ALL accounts\n"
            f"  <code>{p}stop</code>      — Stop ALL accounts\n"
            f"  <code>{p}status</code>    — Global status\n"
            f"  <code>{p}list</code>      — List all accounts\n\n"

            f"{C.PINK}👤 PER-ACCOUNT{C.RESET}\n"
            f"  <code>{p}on sakil1</code>        — Start one\n"
            f"  <code>{p}on sakil1 sakil2</code> — Start multiple\n"
            f"  <code>{p}off sakil1</code>       — Stop one\n"
            f"  <code>{p}off sakil1 sakil2</code>— Stop multiple\n\n"

            f"{C.PINK}🔄 MANUAL{C.RESET}\n"
            f"  <code>{p}rotate sakil1 -100...</code>\n"
            f"  <code>{p}reload</code>    — Reload config\n\n"

            f"{C.DIM}Built by Sakil 💜{C.RESET}"
        )
        await message.edit(text)
