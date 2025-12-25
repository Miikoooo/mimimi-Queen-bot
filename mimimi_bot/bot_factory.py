import discord
from discord.ext import commands


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True

    class MimimiBot(commands.Bot):
        async def setup_hook(self) -> None:
            # Cogs laden (async korrekt)
            from mimimi_bot.cogs.free_games import FreeGamesCog
            from mimimi_bot.cogs.moderation import ModerationCog
            from mimimi_bot.cogs.ui_buttons import UIButtonCog

            await self.add_cog(ModerationCog(self))
            await self.add_cog(UIButtonCog(self))
            await self.add_cog(FreeGamesCog(self))

    bot = MimimiBot(command_prefix=">", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    return bot
