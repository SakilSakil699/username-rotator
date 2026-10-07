"""
⚙️ Auto Handlers
Startup, errors, aur background tasks
"""

import asyncio
from core.logger import log
from core.metrics import metrics
from core.colors import C


def register(app):
    """Register handlers."""

    # ═════════════════════════════════════
    #  AUTO STATUS (har 1 hour)
    # ═════════════════════════════════════
    @app.on_message()
    async def _auto_check(client, message):
        """Placeholder — auto handler."""
        pass

    # ═════════════════════════════════════
    #  DAILY METRICS REPORT
    # ═════════════════════════════════════
    async def daily_report():
        """Send daily stats to owner."""
        from config import OWNER_ID

        while True:
            await asyncio.sleep(86400)  # 24 hours

            m = metrics.summary()
            text = (
                f"{C.PURPLE}📊 <b>Daily Report</b>{C.RESET}\n\n"
                f"⏱ Uptime: <code>{m['uptime']}</code>\n"
                f"🔄 Rotations: <code>{m['rotations']}</code>\n"
                f"❌ Failures: <code>{m['failures']}</code>\n"
                f"📈 Success: <code>{m['success_rate']}</code>\n"
            )

            try:
                await app.send_message(OWNER_ID, text)
            except Exception:
                pass

    # Start background tasks
    asyncio.create_task(daily_report())
    log.info("Background tasks started")
