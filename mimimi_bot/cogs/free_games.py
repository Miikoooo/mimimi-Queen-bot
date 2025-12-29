from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

import aiohttp
import discord
from discord.ext import commands, tasks

from mimimi_bot.config import load_config
from mimimi_bot.services.epic import fetch_epic_free_games
from mimimi_bot.services.steam_store import fetch_steam_store_free_specials
from mimimi_bot.services.steamdb import fetch_steamdb_free_games
from mimimi_bot.services.storage import load_state, save_state

BERLIN = ZoneInfo("Europe/Berlin")
REMINDER_HOURS_DEFAULT = 6


def now_de() -> str:
    return datetime.now(BERLIN).strftime("%d.%m.%Y %H:%M")


class FreeGamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = load_config()

        self.state = load_state() or {}
        self.state.setdefault("posted_ids", [])
        self.state.setdefault("reminded_ids", [])

        self.reminder_hours = REMINDER_HOURS_DEFAULT

        self.daily_epic_post.start()
        self.reminder_check.start()

    def cog_unload(self):
        self.daily_epic_post.cancel()
        self.reminder_check.cancel()

    # EXAKT 17:01 DE: poste nur das "frisch gestartete" Epic-Angebot
    @tasks.loop(time=time(hour=17, minute=1, tzinfo=BERLIN))
    async def daily_epic_post(self):
        channel = self._get_target_channel()
        if channel is None:
            return

        print(f"[FreeGames] daily_epic_post tick {now_de()} (DE)", flush=True)

        posted = set(self.state.get("posted_ids", []))

        async with aiohttp.ClientSession(
            headers={"User-Agent": "mimimi-Queen-bot/1.0"}
        ) as session:
            epic = await fetch_epic_free_games(session=session)

        now_utc = datetime.now(timezone.utc)

        # Robust: falls Epic minimal verzögert oder Restart/Deploy, lassen wir Fenster etwas größer
        fresh_window = timedelta(hours=2)

        active_fresh: List[Dict[str, Any]] = []
        for x in epic:
            start_dt = _parse_dt_utc(x.get("start"))
            end_dt = _parse_dt_utc(x.get("end"))

            if not start_dt:
                continue

            # aktiv?
            if start_dt > now_utc:
                continue
            if end_dt and now_utc > end_dt:
                continue

            # frisch?
            if now_utc - start_dt > fresh_window:
                continue

            active_fresh.append(x)

        # newest first
        active_fresh.sort(
            key=lambda it: _parse_dt_utc(it.get("start"))
            or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )

        new_epic = [x for x in active_fresh if x["id"] not in posted]
        if not new_epic:
            return

        await channel.send(embed=self._bundle("epic", new_epic, "Neues Epic Free Game"))

        for x in new_epic:
            posted.add(x["id"])

        self.state["posted_ids"] = list(posted)
        save_state(self.state)

    @daily_epic_post.before_loop
    async def before_daily_epic_post(self):
        await self.bot.wait_until_ready()

    # Reminder + Steam (stündlich)
    @tasks.loop(hours=1)
    async def reminder_check(self):
        channel = self._get_target_channel()
        if channel is None:
            return

        posted = set(self.state.get("posted_ids", []))
        reminded = set(self.state.get("reminded_ids", []))

        async with aiohttp.ClientSession(
            headers={"User-Agent": "mimimi-Queen-bot/1.0"}
        ) as session:
            epic = await fetch_epic_free_games(session=session)

            try:
                steamdb = await fetch_steamdb_free_games(session=session)
            except Exception:
                steamdb = []

            try:
                steam_store = await fetch_steam_store_free_specials(
                    session=session, limit=8
                )
            except Exception:
                steam_store = []

        all_items = epic + steamdb + steam_store

        # neue Nicht-Epic Deals posten (Epic kommt fix um 17:01)
        new_non_epic = [
            x for x in all_items if x.get("source") != "epic" and x["id"] not in posted
        ]
        if new_non_epic:
            for source, items in _group_by_source(new_non_epic).items():
                await channel.send(embed=self._bundle(source, items, "Neue Free Games"))
            for x in new_non_epic:
                posted.add(x["id"])

        # Reminder (≤ reminder_hours vor Ablauf, einmalig)
        now_utc = datetime.now(timezone.utc)
        cutoff = now_utc + timedelta(hours=self.reminder_hours)

        expiring: List[Dict[str, Any]] = []
        for x in all_items:
            if x["id"] in reminded:
                continue
            end_dt = _parse_dt_utc(x.get("end"))
            if end_dt and now_utc <= end_dt <= cutoff:
                expiring.append(x)

        if expiring:
            for source, items in _group_by_source(expiring).items():
                await channel.send(
                    embed=self._bundle(
                        source, items, f"Reminder (≤ {self.reminder_hours}h)"
                    )
                )
            for x in expiring:
                reminded.add(x["id"])

        self.state["posted_ids"] = list(posted)
        self.state["reminded_ids"] = list(reminded)
        save_state(self.state)

    @reminder_check.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()

    @commands.command(name="free")
    async def free(self, ctx: commands.Context):
        async with aiohttp.ClientSession(
            headers={"User-Agent": "mimimi-Queen-bot/1.0"}
        ) as session:
            epic = await fetch_epic_free_games(session=session)

            try:
                steamdb = await fetch_steamdb_free_games(session=session)
            except Exception:
                steamdb = []

            try:
                steam_store = await fetch_steam_store_free_specials(
                    session=session, limit=8
                )
            except Exception:
                steam_store = []

        if epic:
            await ctx.send(embed=self._bundle("epic", epic, "Aktuell kostenlos"))

        if steamdb:
            await ctx.send(embed=self._bundle("steamdb", steamdb, "Aktuell kostenlos"))
        else:
            status = discord.Embed(
                title="Steam Status",
                description=f"Zuletzt aktualisiert: {now_de()} (DE)",
                color=discord.Color.orange(),
            )
            status.add_field(
                name="SteamDB",
                value="Aktuell keine **Free to Keep** Promotions.",
                inline=False,
            )

            if steam_store:
                status.add_field(
                    name="Steam Store (Fallback)",
                    value=f"{len(steam_store)} Treffer (0€ Specials) – siehe nächstes Embed.",
                    inline=False,
                )
            else:
                status.add_field(
                    name="Steam Store",
                    value="Aktuell keine **0€ Specials** gefunden.",
                    inline=False,
                )

            await ctx.send(embed=status)

            if steam_store:
                await ctx.send(
                    embed=self._bundle(
                        "steam", steam_store, "Steam Fallback (0€ Specials)"
                    )
                )

        if not epic and not steamdb and not steam_store:
            await ctx.send("Gerade nichts gefunden.")

    def _get_target_channel(self) -> Optional[discord.abc.Messageable]:
        channel_id = self.config.free_games_channel_id
        if not channel_id:
            return None
        return self.bot.get_channel(channel_id)

    def _bundle(
        self, source: str, items: List[Dict[str, Any]], title_prefix: str
    ) -> discord.Embed:
        if source == "epic":
            src = "Epic Games"
        elif source == "steamdb":
            src = "Steam (SteamDB)"
        elif source == "steam":
            src = "Steam Store"
        else:
            src = source

        e = discord.Embed(
            title=f"{title_prefix}: {src}",
            description=self._format(items),
            color=discord.Color.green(),
        )
        e.set_footer(text=f"Zuletzt aktualisiert: {now_de()} (DE)")
        return e

    def _format(self, items: List[Dict[str, Any]]) -> str:
        lines: List[str] = []
        for x in items[:10]:
            end_dt = _parse_dt_utc(x.get("end"))
            if end_dt:
                end_de = end_dt.astimezone(BERLIN).strftime("%d.%m.%Y %H:%M")
                lines.append(f"- [{x['title']}]({x['url']}) — endet: {end_de} (DE)")
            else:
                lines.append(f"- [{x['title']}]({x['url']})")
        if len(items) > 10:
            lines.append(f"... und {len(items) - 10} weitere")
        return "\n".join(lines)


def _group_by_source(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {}
    for x in items:
        out.setdefault(x.get("source", "unknown"), []).append(x)
    return out


def _parse_dt_utc(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None

    s = value.strip()

    # Epic ISO Z
    if "T" in s and (s.endswith("Z") or s.endswith("z")):
        try:
            s2 = s.replace("z", "Z")
            if "." in s2:
                s2 = s2.split(".")[0] + "Z"
            dt = datetime.strptime(s2, "%Y-%m-%dT%H:%M:%SZ")
            return dt.replace(tzinfo=timezone.utc)
        except Exception:
            return None

    # SteamDB: "YYYY-MM-DD HH:MM UTC"
    s_no_utc = s.replace("UTC", "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(s_no_utc, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except Exception:
            pass

    return None
