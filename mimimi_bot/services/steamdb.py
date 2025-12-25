import re
from typing import Any, Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup

STEAMDB_FREE_URL = "https://steamdb.info/upcoming/free/"
APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")

# realistischer Browser User-Agent (Windows + Chrome)
STEAMDB_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://steamdb.info/",
    "DNT": "1",
}


async def fetch_steamdb_free_games(
    only_free_to_keep: bool = True,
    session: Optional[aiohttp.ClientSession] = None,
) -> List[Dict[str, Any]]:
    close_session = False
    if session is None:
        close_session = True
        session = aiohttp.ClientSession()

    try:
        async with session.get(
            STEAMDB_FREE_URL, headers=STEAMDB_HEADERS, timeout=25
        ) as r:
            # SteamDB blockt manchmal automatisiert -> dann einfach leer zurückgeben
            if r.status in (403, 429):
                return []
            r.raise_for_status()
            html = await r.text()

        soup = BeautifulSoup(html, "html.parser")

        results: Dict[str, Dict[str, Any]] = {}

        for a in soup.find_all("a", href=True):
            href = a["href"]
            m = APP_RE.search(href)
            if not m:
                continue

            app_id = m.group(1)
            url = href.split("?")[0]
            title = a.get_text(strip=True) or f"Steam App {app_id}"

            container = a.find_parent(["div", "tr", "li", "section"]) or a.parent
            context_text = container.get_text(" ", strip=True) if container else ""

            promo_type = None
            if "Free to Keep" in context_text:
                promo_type = "Free to Keep"
            elif "Play For Free" in context_text:
                promo_type = "Play For Free"

            if only_free_to_keep and promo_type != "Free to Keep":
                continue

            started = _extract_after_label(context_text, "Started:")
            expires = _extract_after_label(context_text, "Expires:")

            results[app_id] = {
                "id": f"steamdb:{app_id}",
                "source": "steamdb",
                "title": title,
                "url": url,
                "start": started,
                "end": expires,
                "type": promo_type or "Promotion",
            }

        return list(results.values())

    finally:
        if close_session:
            await session.close()


def _extract_after_label(text: str, label: str) -> Optional[str]:
    idx = text.find(label)
    if idx == -1:
        return None
    tail = text[idx + len(label) :].strip()
    for stop in ("Started:", "Expires:", "Free to Keep", "Play For Free"):
        stop_idx = tail.find(stop)
        if stop_idx != -1:
            tail = tail[:stop_idx].strip()
    return tail if tail else None
