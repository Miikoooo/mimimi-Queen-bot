from typing import Any, Dict, List, Optional

import aiohttp

EPIC_FREE_JSON = (
    "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"
)


async def fetch_epic_free_games(
    country: str = "DE",
    locale: str = "en-US",
    session: Optional[aiohttp.ClientSession] = None,
) -> List[Dict[str, Any]]:
    """
    Liefert nur Einträge, die aktuell wirklich 0€ (free to keep) sind.
    Rückgabeformat passt zu FreeGamesCog.
    """
    close_session = False
    if session is None:
        close_session = True
        session = aiohttp.ClientSession(headers={"User-Agent": "mimimi-Queen-bot/1.0"})

    try:
        params = {"locale": locale, "country": country, "allowCountries": country}
        async with session.get(EPIC_FREE_JSON, params=params, timeout=25) as r:
            r.raise_for_status()
            data = await r.json()

        elements = (
            data.get("data", {})
            .get("Catalog", {})
            .get("searchStore", {})
            .get("elements", [])
        )

        results: List[Dict[str, Any]] = []
        for el in elements:
            promos = el.get("promotions")
            if not promos:
                continue

            promo_offers = promos.get("promotionalOffers") or []
            if not promo_offers:
                continue

            offers = promo_offers[0].get("promotionalOffers") or []
            if not offers:
                continue

            # Preis prüfen
            price_info = el.get("price", {}).get("totalPrice", {})
            if price_info.get("discountPrice") != 0:
                continue

            title = el.get("title") or "Unknown"
            game_id = el.get("id") or title

            # URL bestimmen
            product_slug = el.get("productSlug")
            if not product_slug:
                mappings = el.get("catalogNs", {}).get("mappings", [])
                if mappings:
                    product_slug = mappings[0].get("pageSlug")

            url = (
                f"https://store.epicgames.com/p/{product_slug}"
                if product_slug
                else "https://store.epicgames.com/"
            )

            offer = offers[0]
            start = offer.get("startDate")  # ISO UTC
            end = offer.get("endDate")  # ISO UTC

            promo_key = start or "no-start"
            item_id = f"epic:{game_id}:{promo_key}"

            results.append(
                {
                    "id": item_id,
                    "source": "epic",
                    "title": title,
                    "url": url,
                    "start": start,
                    "end": end,
                }
            )

        return results

    finally:
        if close_session:
            await session.close()
