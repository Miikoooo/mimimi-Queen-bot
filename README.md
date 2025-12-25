# mimimi Queen Bot 👑

Ein privater Discord-Bot in Python mit Fokus auf:

- Free Games (Epic Games, SteamDB, Steam Store Fallback)
- einfache Moderation
- UI-Buttons
- saubere, modulare Struktur (Cogs + Services)

Der Bot checkt automatisch nach neuen Free Games und postet sie in einen definierten Channel.

---

## Features

### Free Games

- **Epic Games**: automatische Free-to-Keep Spiele
- **SteamDB**: echte „Free to Keep“-Promotions (wenn vorhanden)
- **Steam Store Fallback**: 0€-Specials, falls SteamDB leer ist
- **Stündlicher Check**
- **Reminder** vor Ablauf (Standard: 6h)
- Duplikat-Schutz über `state.json`
- Zeiten in **Deutschland (Europe/Berlin)**

Command:

---

### Moderation

- `,ping`
- `,purge <anzahl>`
- Berechtigungen werden geprüft

---

### UI

- Test-Button mit Discord `View` / `Button`

---

## Voraussetzungen

- Python **3.12+** (3.14 funktioniert ebenfalls)
- Discord Bot Token
- Internetzugang (Epic / Steam)

---

## Installation

```bash
git clone https://github.com/Miikoooo/mimimi-Queen-bot.git
cd mimimi-Queen-bot

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install tzdata

DISCORD_TOKEN=dein_discord_token
FREE_GAMES_CHANNEL_ID=123456789012345678
```

---

## .env example

DISCORD_TOKEN=put_your_token_here
FREE_GAMES_CHANNEL_ID=123456789012345678

---

## License

MIT License

Copyright (c) 2025

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


