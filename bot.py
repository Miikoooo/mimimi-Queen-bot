import discord
from discord.ext import commands
import youtube_dl
import asyncio

from Music import Music



TOKEN = 'MTAxNTI2ODM5NzgxMjA0MzgwNg.G1uupO.dZ6kETbAfxPAW2dHzJsLHClf7y-tvfiAWqd0x4'

client = commands.Bot(command_prefix = ",", intents=discord.Intents.all())



##Bot ist Online
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('adding trash commands'))
    print ('----------------')

#User ist auf den Server eingetroffen.
@client.event
async def on_member_join(member):
    print("f'{member} ist der Kirche beigetreten.")

#User hat den Server verlassen.
@client.event
async def on_member_remove(member):
    print("f'{member} ist ein Atheist geworden.")

#Kann x Anzahl vorheriger Nachrichten löschen
@client.command()
async def purge(ctx, limit=50, member: discord.Member=None):#
    """Delete up to 50 messages"""
    await ctx.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await ctx.send("Please pass in an integer as limit")
    if not member:
        await ctx.channel.purge(limit=limit)
        return await ctx.send(f"Purged {limit} messages", delete_after=3)
    async for m in ctx.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)

#Bot joint VC
@client.command(pass_context=True)    
async def join_channel(ctx):
    """Joins a voice channel"""
    channel = ctx.author.voice.channel
    await channel.connect()

#Bot leaved VC
@client.command()
async def leave(ctx): 
    """Leaves a voice channel"""
    await ctx.voice_client.disconnect()
    


async def main():
    async with client:
        await client.add_cog(Music(client))
        await client.start(TOKEN)


asyncio.run(main())
