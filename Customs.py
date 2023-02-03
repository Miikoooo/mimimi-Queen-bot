import discord
from discord.ext import commands
from discord.ui import View, Button
import random

class Customs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def generate(self, ctx, *players: str):
        """generates teams e.g. /generate [Player1] [Player2] [Player3] ..."""
        players = list(players)
        random.shuffle(players)
        team_size = len(players) // 2
        team_1 = players[:team_size]
        team_2 = players[team_size:]
        await ctx.send(f"Team 1: {', '.join(team_1)}")
        await ctx.send(f"Team 2: {', '.join(team_2)}")

   
