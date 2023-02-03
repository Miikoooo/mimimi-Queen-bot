import discord
from discord.ext import commands
from discord.ui import View, Button

import discord
from discord.ext import commands

class Customs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def generate(self, ctx, *players: str):
        '''Generates Teams e.g. /generate [Player1] [Player2] [Player3] ...'''
        if len(players) % 2 == 1:
            await ctx.send("An odd number of players cannot be divided equally into two teams")
            return
        
        first_team = players[:len(players)//2]
        second_team = players[len(players)//2:]
        
        await ctx.send(f"Team 1: {', '.join(first_team)}\nTeam 2: {', '.join(second_team)}")



   
