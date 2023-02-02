import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button


class Customs(commands.Cog):
    def __init__(self, client):
        self.client = client
        @client.command()
        async def customs(ctx):
            '''Erstellen ein Custom'''
            button = Button(style=discord.ButtonStyle.primary, label="Start")
            view = View()
            view.add_item(button)
            await ctx.send('test', view=view)    
