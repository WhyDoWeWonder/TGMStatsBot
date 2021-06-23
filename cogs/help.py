import requests
import discord
import os
import aiohttp
import asyncio
import json
import datetime as dt
import time
from ago import human
from ago import delta2dict
from datetime import datetime
from discord.ext.commands import cooldown, BucketType
import datetime
from discord.ext import commands

class Help(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('test')

    @commands.command()
    async def help(self, ctx: commands.context):
        if ctx.channel.id == 856589752584503300:
            async with ctx.typing():
                            page1 = discord.Embed(title="", color=0xbc2a82)
                            page1.set_author(name="Cylone Stats Bot Help Menu 1/2")
                            page1.add_field(name="Stats", value="Displays latest game and player stats on team games", inline=True)
                            page1.timestamp = datetime.datetime.utcnow()
                            page1.set_footer(text='Bot Created by ksndq#8052', icon_url="https://cdn.discordapp.com/avatars/431703739913732097/013868d08ceb35bf90fb568bfbd1e854.png?size=64")
                            page1.set_image(url="https://cdn.discordapp.com/avatars/854744409253216277/fee6f1ed242feb3d465162d8e9e393a4.png?size=128")
                            ################################################################
                            page2 = discord.Embed(title="", color=0xbc2a82)
                            page2.set_author(name="Credit List 2/2")
                            page2.add_field(name="Main Developer", value="<@431703739913732097> <:ksndq:856587427283337236>", inline=False)
                            page2.add_field(name="Side Developer", value="<@336363923542376449> <:LordofLightning:856587426985934910>", inline=False)
                            page2.add_field(name="Tester", value="<@491621008856449044> <:THAWERZ:856589646909669427>", inline=False)
                            page2.set_footer(text='Bot Created by ksndq#8052', icon_url="https://cdn.discordapp.com/avatars/431703739913732097/013868d08ceb35bf90fb568bfbd1e854.png?size=64")
        else:
            embedVar = discord.Embed(title="You can't use that here!", color=0xFF0000)
            await ctx.send(embed=embedVar, delete_after=5.0)
            await ctx.message.delete()
            pass

        pages = [page1, page2]
        message = await ctx.send(embed = page1)
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        def check(reaction, user):
            return user == ctx.author
        i = 0
        reaction = None
        while True:
            if str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed = pages[i])
            elif str(reaction) == '▶':
                if i < 1:
                    i += 1
                    await message.edit(embed = pages[i])
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout = 45.0, check = check)
                await message.remove_reaction(reaction, user)
            except:
                break
        await message.clear_reactions()

def setup(client):
    client.add_cog(Help(client))