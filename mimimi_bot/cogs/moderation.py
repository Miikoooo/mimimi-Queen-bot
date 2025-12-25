from __future__ import annotations

from discord.ext import commands


class ModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

    @commands.command(name="purge", aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = 10) -> None:
        amount = max(1, min(amount, 200))
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 für den command selbst
        await ctx.send(f"{len(deleted) - 1} gelöscht.", delete_after=3)

    @purge.error
    async def purge_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Darfst du nicht.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Zahl angeben.")
        else:
            await ctx.send("Fehler.")
