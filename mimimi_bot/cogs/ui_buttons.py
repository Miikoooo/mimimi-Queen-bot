from __future__ import annotations

import discord
from discord.ext import commands


class UIButtonCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="button")
    async def button(self, ctx: commands.Context) -> None:
        class TestView(discord.ui.View):
            @discord.ui.button(label="Klick", style=discord.ButtonStyle.primary)
            async def ok(self, interaction: discord.Interaction, _: discord.ui.Button):
                await interaction.response.send_message("ok", ephemeral=True)

        await ctx.send("Button:", view=TestView())
