import re
from typing import Any, Dict, List, Optional

import aiohttp
from bs4 import BeautifulSoup

STEAM_SEARCH_URL = "https://store.steampowered.com/search/"
APP_RE = re.compile(r"/app/(\d+)")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
}


async def fetch_steam_store_free_specials(
    session: Optional[aiohttp.ClientSession] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Steam Store Search: maxprice=free + specials=1
    Das sind Deals, die im Store gerade 0€ sind (nicht immer "free to keep" garantiert, aber oft).
    """
    close_session = False
    if session is None:
        close_session = True
        session = aiohttp.ClientSession()

    try:
        params = {"maxprice": "free", "specials": "1", "category1": "998"}
        async with session.get(
            STEAM_SEARCH_URL, params=params, headers=HEADERS, timeout=25
        ) as r:
            r.raise_for_status()
            html = await r.text()

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.select("a.search_result_row")

        results: List[Dict[str, Any]] = []
        for row in rows[:limit]:
            href = row.get("href")
            if not href:
                continue

            m = APP_RE.search(href)
            app_id = m.group(1) if m else href

            title_el = row.select_one("span.title")
            title = title_el.get_text(strip=True) if title_el else "Steam Deal"

            results.append(
                {
                    "id": f"steam:{app_id}",
                    "source": "steam",
                    "title": title,
                    "url": href.split("?")[0],
                    "start": None,
                    "end": None,
                    "type": "Free (Store Specials)",
                }
            )

        return results
    finally:
        if close_session:
            await session.close()
