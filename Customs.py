import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button


class Customs(commands.Cog):
    def __init__(self, client):
        self.client = client
        
        @client.command()
        async def custom(ctx):
            '''Erstelle ein Custom'''
            button1 = Button(style=discord.ButtonStyle.green, label="Start", emoji= '🎲')
            button2 = Button(style=discord.ButtonStyle.red, label="Cancel", emoji= '☠️')
            view = View()
            view.add_item(button1)
            view.add_item(button2)

            async def button1_callback(interaction):
                await interaction.response.send_message('Let the dice decide!')
                await interaction.response.followup.send('Let the dice decide!')


            button1.callback = button1_callback

            async def button2_callback(interaction):
                await interaction.response.edit_message(content='Schwach', view=None)

            button2.callback = button2_callback
                




            await ctx.send('Balacing approved vom Riot Balancing Team', view=view)    
