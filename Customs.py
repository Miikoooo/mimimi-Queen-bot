import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button


class Customs(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        #@client.command()
        async def custom(ctx):
            '''Erstelle ein Custom'''
            button1 = Button(style=discord.ButtonStyle.green, label="Start")
            button2 = Button(style=discord.ButtonStyle.red, label="Cancel")
            view = View()
            view.add_item(button1)
            view.add_item(button2)
            await ctx.send('Balacing approved vom Riot Balancing Team', view=view)    
