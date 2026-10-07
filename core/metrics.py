"""
📊 Metrics Tracker
Live stats — success, failures, uptime
"""

import time
from collections import defaultdict


class Metrics:
    def __init__(self):
        self.start_time = time.time()
        self.rotations = 0
        self.failures = 0
        self.per_account = defaultdict(int)
        self.per_channel = defaultdict(int)
        self.recent = []  # last 10 events

    def record_success(self, account, channel, username):
        """Record successful rotation."""
        self.rotations += 1
        self.per_account[account] += 1
        self.per_channel[channel] += 1
        self.recent.append({
            "time": time.time(),
            "account": account,
            "channel": channel,
            "username": username,
            "status": "✅",
        })
        self.recent = self.recent[-10:]

    def record_failure(self, account, channel, error):
        """Record failed rotation."""
        self.failures += 1
        self.recent.append({
            "time": time.time(),
            "account": account,
            "channel": channel,
            "username": str(error)[:50],
            "status": "❌",
        })
        self.recent = self.recent[-10:]

    @property
    def uptime(self):
        sec = int(time.time() - self.start_time)
        h, r = divmod(sec, 3600)
        m, s = divmod(r, 60)
        return f"{h}h {m}m {s}s"

    @property
    def uptime_seconds(self):
        return int(time.time() - self.start_time)

    @property
    def success_rate(self):
        total = self.rotations + self.failures
        if total == 0:
            return "100.0%"
        return f"{(self.rotations / total) * 100:.1f}%"

    def summary(self):
        """Get summary dict."""
        return {
            "uptime": self.uptime,
            "uptime_seconds": self.uptime_seconds,
            "rotations": self.rotations,
            "failures": self.failures,
            "success_rate": self.success_rate,
            "accounts": len(self.per_account),
            "channels": len(self.per_channel),
        }

    def top_accounts(self, n=3):
        """Get top N accounts by rotations."""
        return sorted(
            self.per_account.items(),
            key=lambda x: -x[1]
        )[:n]

    def top_channels(self, n=3):
        """Get top N channels by rotations."""
        return sorted(
            self.per_channel.items(),
            key=lambda x: -x[1]
        )[:n]


# Global instance
metrics = Metrics()
