<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24,30&height=220&section=header&text=Username%20Rotator&fontSize=75&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Multi-Account%20Rotation%20Engine&descAlignY=58&descSize=22" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=22&duration=2800&pause=800&color=A78BFA&center=true&vCenter=true&multiline=true&width=850&height=120&lines=%F0%9F%94%84+Automatic+Username+Rotation;%F0%9F%91%A5+Multi-Account+Support;%F0%9F%93%A2+Unlimited+Channels;%F0%9F%94%90+AES-128+Session+Vault;%E2%9A%A1+Async+Parallel+Engine;%F0%9F%92%9C+Built+by+Sakil" alt="Typing SVG" />

**Ek deploy. Saare accounts. Saare channels. Fully automatic.**

<br>

[![Made by Sakil](https://img.shields.io/badge/Made%20by-Sakil-A78BFA?style=for-the-badge&logo=starship&logoColor=white)](https://t.me/YO_UR_OFFICIAL_CRUSH)
[![Telegram](https://img.shields.io/badge/Telegram-@YO__UR__OFFICIAL__CRUSH-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/YO_UR_OFFICIAL_CRUSH)
[![GitHub](https://img.shields.io/badge/GitHub-SakilSakil699-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SakilSakil699)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0.106-A78BFA?style=for-the-badge)](https://pyrogram.org)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-22C55E?style=for-the-badge)]()
[![Termux](https://img.shields.io/badge/Termux-Ready-000000?style=for-the-badge&logo=termux)]()

</div>

---

<div align="center">

## ✨ Features

</div>

<table>
<tr>
<td width="50%" valign="top">

### 🔄 Core Engine

- ♻️ **Auto Rotation** — Set interval, forget it
- 👥 **Multi-Account** — 1-100+ accounts
- 📢 **Multi-Channel** — Unlimited channels
- ⚡ **Parallel Async** — All channels independent
- 🎯 **Per-Channel Config** — Alag interval, alag pool
- 🔁 **Auto Recovery** — Crash hone pe khud restart

</td>
<td width="50%" valign="top">

### 🔐 Security

- 🔒 **AES-128 Vault** — Fernet encrypted sessions
- 🛡️ **Stolen Session Safe** — Bina VAULT_KEY useless
- 🔑 **Encrypted `.env`** — chmod 600 auto
- 🚫 **Owner-Only Commands** — Sensitive actions protected
- 📝 **No Plain Logs** — Session kabhi log nahi hoti

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 Monitoring

- 📈 **Live Dashboard** — Real-time stats
- 🏆 **Top Performers** — Best accounts
- 📉 **Success Rate** — Live calculation
- 🕐 **Recent Activity** — Last 10 events
- ⏱ **Uptime Tracking** — Precise
- 📨 **Telegram Alerts** — Har rotation pe notify

</td>
<td width="50%" valign="top">

### 🎮 Control

- 🎯 **Manual Rotate** — Force immediate change
- 🔄 **Hot Reload** — Config change, no restart
- 🛑 **Stop All** — Emergency stop
- 📋 **List Accounts** — Quick overview
- 📢 **List Channels** — Quick overview
- 👤 **Account Detail** — Username, ID, phone

</td>
</tr>
</table>

---

## 🎬 How It Works

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    📱 Tumhara Telegram Account (Main Userbot)                ║
║         │                                                    ║
║         ▼                                                    ║
║    ┌──────────────────────────────────────────────┐          ║
║    │  🤖 Username Rotator Engine                   │          ║
║    │                                              │          ║
║    │  ┌──────────────────────────────────────┐   │          ║
║    │  │  📂 rotations.json                    │   │          ║
║    │  │  ├─ Account 1 → Channel A, B, C       │   │          ║
║    │  │  ├─ Account 2 → Channel D             │   │          ║
║    │  │  └─ Account 7 → Channel J             │   │          ║
║    │  └──────────────────────────────────────┘   │          ║
║    │                                              │          ║
║    │  ┌──────────────────────────────────────┐   │          ║
║    │  │  🔄 Parallel Rotation Loops          │   │          ║
║    │  │                                      │   │          ║
║    │  │  Account 1/Channel A ──┐             │   │          ║
║    │  │  Account 1/Channel B ──┼─ 1 hour     │   │          ║
║    │  │  Account 2/Channel D ──┤  interval   │   │          ║
║    │  │  ...                   │             │   │          ║
║    │  │  Account 7/Channel J ──┘             │   │          ║
║    │  └──────────────────────────────────────┘   │          ║
║    └──────────────────────────────────────────────┘          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Simple words me:**

1. **Tumhare saare accounts** `accounts/` folder me ya `.env` me saved hain
2. **`rotations.json`** batati hai kaunsa account kaunse channel ko handle karega
3. **Bot start hone pe**, har account login hota hai
4. **Har channel ke liye** ek **independent loop** chalta hai
5. **Har interval** (default 1 hour) pe **username automatically** change hota hai
6. **Tumhe notification** aata hai Telegram pe

---

## 🚀 Quick Start

### 📱 Termux (Android)

<details>
<summary><b>👉 Click karo — Poori Termux guide</b></summary>

<br>

**Step 1: Termux install karo**
- ❌ **Play Store se MAT karo** (outdated hai)
- ✅ **[F-Droid](https://f-droid.org/packages/com.termux/)** se karo

**Step 2: Update + tools**

```bash
pkg update && pkg upgrade -y
pkg install -y python python-pip git nano curl wget openssl libffi rust clang make binutils tmux
```

**Step 3: Heavy packages**

```bash
pkg install -y python-cryptography
```

**Step 4: Pip packages**

```bash
pip install --break-system-packages pyrogram tgcrypto python-dotenv cryptography
```

**Step 5: Storage + wakelock**

```bash
termux-setup-storage
termux-wake-lock
```

**Step 6: Clone repo**

```bash
cd ~
git clone https://github.com/SakilSakil699/username-rotator.git
cd username-rotator
```

**Step 7: Setup**

```bash
cp .env.example .env
nano .env
# API_ID, API_HASH, SESSION_STRING, OWNER_ID, VAULT_KEY daalo
```

**Step 8: Session generate**

```bash
python gen_session.py --name main
python gen_session.py --name sakil1
python gen_session.py --name sakil2
# ... jitne accounts
```

**Step 9: Move sessions**

```bash
mkdir -p accounts
mv sessions/*.session accounts/
```

**Step 10: rotations.json banao**

Upar wala example dekho, apne channels add karo.

**Step 11: Background me chalao**

```bash
tmux new -s rotator
python main.py
# Detach: Ctrl+B, D
# Reattach: tmux attach -t rotator
```

</details>

### ☁️ VPS (Ubuntu/Debian)

```bash
# Update
sudo apt update && sudo apt install -y python3 python3-pip git

# Clone
git clone https://github.com/SakilSakil699/username-rotator.git
cd username-rotator

# Install
pip3 install -r requirements.txt

# Setup .env
cp .env.example .env
nano .env

# Sessions
python3 gen_session.py --name main
python3 gen_session.py --name sakil1

# Run
python3 main.py
```

### 🐳 Docker

```bash
docker build -t username-rotator .
docker run -d --name rotator \
  --restart unless-stopped \
  -v $(pwd)/accounts:/app/accounts \
  -v $(pwd)/.env:/app/.env \
  username-rotator
```

---

## 📁 Project Structure

```
username-rotator/
│
├── 📄 main.py                  Entry point
├── 📄 config.py                Config loader
├── 📄 gen_session.py           Session generator
├── 📄 rotations.json           ⭐ MAIN CONFIG
├── 📄 requirements.txt
├── 📄 .env                     Secrets (never commit)
├── 📄 .env.example
├── 📄 .gitignore
├── 📄 README.md
│
├── 📂 core/                    Engine
│   ├── banner.py               ASCII startup
│   ├── colors.py               Terminal colors
│   ├── logger.py               Beautiful logs
│   ├── metrics.py              Stats tracker
│   ├── session_vault.py        AES-128 encryption
│   └── rotation_manager.py     🔄 Main engine
│
├── 📂 modules/                 Commands
│   ├── commands.py             All bot commands
│   ├── handlers.py             Background tasks
│   └── utils.py                Helpers
│
├── 📂 accounts/                Session files
│   ├── sakil1.session
│   ├── sakil2.session
│   └── ...
│
├── 📂 data/                    Runtime data
└── 📂 logs/                    Log files
```

---

## ⚙️ Configuration

### `.env`

```env
# ═══ Main Userbot ═══
API_ID=123456
API_HASH=your_api_hash_here
SESSION_STRING=your_main_session
OWNER_ID=your_telegram_id

# ═══ Security ═══
VAULT_KEY=your-32-char-random-key

# ═══ Multi-Account Sessions (optional) ═══
# SESSION_SAKIL1=gAAAAAB...
# SESSION_SAKIL2=gAAAAAB...
```

### `rotations.json` — Structure

```json
{
  "accounts": {
    "sakil1": {                          ← Account name
      "channels": [
        {
          "channel_id": -1002461966751,  ← Channel ID
          "interval": 3600,              ← Seconds (1 hour)
          "enabled": true,               ← ON/OFF
          "_note": "Friends",            ← Your note
          "pool": [                      ← Usernames to rotate
            "sakilAnowar1",
            "sakilAnowar2",
            "sakilAnowar3"
          ]
        }
      ]
    }
  }
}
```

### 🔑 `VAULT_KEY` Generate Karo

```bash
python -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"
```

Output example:
```
dGhpcyBpcyBhIHN1cGVyIHNlY3VyZSBrZXkgZm9yIHlvdQ==
```

`.env` me paste karo: `VAULT_KEY=dGhpcyBpcyBh...`

---

## 🎮 Commands

<div align="center">

| Command | Description |
|:-------:|:------------|
| `.start` `.help` | Show all commands |
| `.status` | 📊 Live dashboard |
| `.metrics` | 📈 Detailed stats |
| `.uptime` | ⏱ Bot uptime |
| `.ping` | 🏓 Latency check |
| `.accounts` | 👥 List all accounts |
| `.channels` | 📢 List all channels |
| `.acc <name>` | 👤 Account detail |
| `.rotate <acc> <ch>` | 🔄 Manual rotate |
| `.reload` | ♻️ Reload `rotations.json` |
| `.stop` | 🛑 Stop all rotations |
| `.restart` | 🔁 Restart bot |
| `.encrypt <s>` | 🔐 Encrypt session |
| `.decrypt <s>` | 🔓 Decrypt session (owner only) |

</div>

---

## 🔐 Security

### Session Vault — How It Works

```
Your Session String
       │
       ▼
┌──────────────────────┐
│  SHA256(VAULT_KEY)   │  ← Key derivation
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Fernet (AES-128)    │  ← Encryption
└──────────┬───────────┘
           │
           ▼
    gAAAAAB...xyz          ← Encrypted
```

**Kisi ne tumhari encrypted session chura bhi li — bina `VAULT_KEY` ke kuch nahi kar sakta.**

### 🛡️ Safety Checklist

- [ ] `VAULT_KEY` set kiya `.env` me (32+ chars)
- [ ] `.env` `.gitignore` me hai
- [ ] `chmod 600 .env` chalaya
- [ ] 2FA enabled Telegram pe
- [ ] Secondary accounts use kar rahe ho
- [ ] Sessions kabhi share nahi kiye
- [ ] Regular backup (encrypted `.7z`)

### 🚨 Never Do This

| ❌ Never | ✅ Always |
|---------|----------|
| Session string kisi ko bhejna | `.env` me rakhna |
| `.env` GitHub pe push | `.gitignore` me daalo |
| Screenshot lena | Sirf encrypted backup |
| Same account 100 IPs pe | Per-account proxy |
| Bulk actions spam | 30+ min interval |

---

## 📚 Examples

### Example 1: Single Account, Single Channel

```json
{
  "accounts": {
    "sakil1": {
      "channels": [
        {
          "channel_id": -1002461966751,
          "interval": 3600,
          "enabled": true,
          "pool": ["mychannel1", "mychannel2"]
        }
      ]
    }
  }
}
```

### Example 2: Single Account, Multiple Channels

```json
{
  "accounts": {
    "sakil1": {
      "channels": [
        { "channel_id": -1001111111111, "interval": 3600, "enabled": true, "pool": ["c1name1", "c1name2"] },
        { "channel_id": -1002222222222, "interval": 3600, "enabled": true, "pool": ["c2name1", "c2name2"] }
      ]
    }
  }
}
```

### Example 3: Multiple Accounts, Multiple Channels

```json
{
  "accounts": {
    "sakil1": {
      "channels": [
        { "channel_id": -1001111111111, "interval": 3600, "enabled": true, "pool": ["a1c1name1"] }
      ]
    },
    "sakil2": {
      "channels": [
        { "channel_id": -1002222222222, "interval": 3600, "enabled": true, "pool": ["a2c1name1"] },
        { "channel_id": -1003333333333, "interval": 3600, "enabled": true, "pool": ["a2c2name1"] }
      ]
    }
  }
}
```

### Example 4: Testing (2 min interval)

```json
{
  "channel_id": -1002461966751,
  "interval": 120,
  "enabled": true,
  "pool": ["sakil1", "sakil2", "sakil3"]
}
```

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ <code>CHAT_ADMIN_REQUIRED</code></b></summary>

**Reason:** Userbot account channel ka **owner nahi** hai.

**Fix:**
1. Channel kholo → Manage → Administrators
2. Userbot account add karo
3. **"Change Channel Info"** permission ON karo
4. Save

</details>

<details>
<summary><b>❌ <code>USERNAME_OCCUPIED</code></b></summary>

**Reason:** Username already kisi aur ne le liya.

**Fix:** Pool se wo username hatao, aur koi unique daalo.

</details>

<details>
<summary><b>❌ <code>FLOOD_WAIT_X</code></b></summary>

**Reason:** Telegram rate limit.

**Fix:** Bata diye seconds **wait karo**. Interval badhao — **minimum 30 minutes**.

</details>

<details>
<summary><b>❌ <code>PEER_ID_INVALID</code></b></summary>

**Reason:** Channel ID galat hai ya account us channel me nahi hai.

**Fix:**
1. `@userinfobot` se confirm karo channel ID
2. Userbot account channel me add karo
3. Bot restart karo

</details>

<details>
<summary><b>❌ <code>AuthKeyUnregistered</code></b></summary>

**Reason:** Session revoke ho gayi.

**Fix:**
```bash
python gen_session.py --name sakil1
```

</details>

<details>
<summary><b>❌ <code>platform android is not supported</code></b></summary>

**Reason:** Termux pe kuch libraries build nahi hoti.

**Fix:**
```bash
pkg install python-cryptography
pip install --break-system-packages pyrogram tgcrypto python-dotenv
```

</details>

<details>
<summary><b>❌ <code>RuntimeError: no current event loop</code></b></summary>

**Reason:** Python 3.14 ne behavior badla.

**Fix:** `main.py` ke top pe:
```python
import asyncio
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
```

</details>

---

## 🎯 Common Tasks

### Naya Account Add Karo

```bash
# 1. Session generate
python gen_session.py --name sakil3

# 2. Move to accounts/
mv sessions/sakil3.session accounts/

# 3. rotations.json me add
nano rotations.json
# "sakil3": { "channels": [...] } add karo

# 4. Reload
# Telegram: .reload
```

### Naya Channel Add Karo

```bash
# 1. rotations.json kholo
nano rotations.json

# 2. Existing account me channel add karo
# "channels": [ { new channel }, { existing } ]

# 3. Save + reload
# Telegram: .reload
```

### Interval Change Karo

```json
"interval": 3600     → "interval": 7200    (2 hours)
"interval": 3600     → "interval": 1800    (30 min)
```

### Emergency Stop

```
.stop
```

Ya `Ctrl+C` Termux me.

---

## 🛣️ Roadmap

- [x] Multi-account rotation
- [x] Multi-channel per account
- [x] AES-128 session vault
- [x] Live dashboard
- [x] Per-channel config
- [x] Owner notifications
- [ ] Proxy per account
- [ ] Web dashboard
- [ ] Redis-backed persistence
- [ ] Auto index save/restore
- [ ] Webhook integration

---

## 🤝 Contributing

Contributions welcome!

1. Fork karo: [github.com/SakilSakil699/username-rotator](https://github.com/SakilSakil699/username-rotator)
2. Branch banao: `git checkout -b feature/amazing`
3. Commit: `git commit -m "Add amazing feature"`
4. Push: `git push origin feature/amazing`
5. Pull Request kholo

### Code Style

- PEP 8
- Type hints
- Docstrings
- Test before submitting

---

## ⚠️ Disclaimer

<div align="center">

### 🚨 EDUCATIONAL PURPOSE ONLY 🚨

</div>

- ❌ Using userbots violates [Telegram ToS](https://telegram.org/tos)
- ⚠️ **Your accounts may be banned**
- 🚫 **Do not** use for spam or abuse
- 🛡️ **Use only on your own accounts**
- 📜 **Author not responsible** for any misuse

**Use at your own risk.**

---

## 📜 License

```
MIT License

Copyright (c) 2025 Sakil (SakilSakil699)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24,30&height=120&section=footer&text=Thanks%20for%20visiting!&fontSize=32&fontColor=ffffff&animation=fadeIn" width="100%"/>

### ⭐ Agar useful lage, **star** dena!

<br>

**Made with ❤️ by [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH)**

[![GitHub](https://img.shields.io/badge/GitHub-SakilSakil699-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SakilSakil699)
[![Telegram](https://img.shields.io/badge/Telegram-@YO__UR__OFFICIAL__CRUSH-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/YO_UR_OFFICIAL_CRUSH)

[⬆ Back to Top](#-username-rotator)

</div>
