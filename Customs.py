
import typing
import random, sys
import asyncio


from distutils.command.check import check

import discord
from discord import ActionRow, Button, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View

client = commands.Bot(command_prefix = ",", intents=discord.Intents.all())

class Customs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        @commands.command()
        async def customs(ctx):
            button = Button(style=ButtonStyle.primary, label="Start")
            view = View()
            view.add_item(button)
            await ctx.send('Hi', view=view)











