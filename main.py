import requests
import discord
import os
import aiohttp
import asyncio
import json
import datetime as dt
import time
import random
import humanize
from discord.ext.commands import cooldown, BucketType
import timedelta
import pprint
import datetime
import timeago, datetime
from datetime import date, timedelta
from discord.ext import commands

intents = discord.Intents.all()

with open("./config.json", mode="r") as fl:
    config = json.loads(fl.read()) 

client = commands.Bot(command_prefix=config["bot"]["prefix"], intents=intents, case_insensitive=True)

client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="CyloneMC.net"))
    print(f'{client.user} has connected to Discord!')

colors = [0x9400D3, 0x4B0082, 0x0000FF, 0x00FF00, 0xFFFF00, 0xFF0000]

now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)

date = datetime.datetime.now()

########################################################################

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def stats(ctx: commands.Context, mc_name : str):
    if ctx.channel.id == 765849289817456651:
            async with ctx.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://tgmapi.cylonemc.net/mc/player/' + mc_name, ) as r:
                        res = await r.json()
                        #######
                        skin = res['user']['uuid']
                        ms = res['user']['lastOnlineDate']
                        ms2 = res['user']['initialJoinDate']
                        win = res['user']['wins']
                        lost = res['user']['losses']
                        k = res['user']['kills']
                        d = res['user']['deaths']
                        #######
                        page1 = discord.Embed(title="", color=0xbc2a82)
                        page1.set_author(name=mc_name + " Stats on The Cylone Network")
                        page1.add_field(name="<a:played:853633469014605824> Matches played", value=(res['user']['matches']), inline=True)
                        page1.add_field(name="<a:kills:853628582731186177> Kills", value=(res['user']['kills']), inline=True)
                        page1.add_field(name="<a:deaths:855109742288437250> Deaths", value=(res['user']['deaths']), inline=True)
                        kd = "{:.2f}".format(k/d)
                        page1.add_field(name="<a:kd:855110404735893515> K/D", value=kd, inline=True)
                        page1.add_field(name="<a:level:853628581188337666> Level", value=(res['user']['level']), inline=True)
                        page1.add_field(name="<a:wins:853628581698600961> Wins", value=(res['user']['wins']), inline=True)
                        page1.add_field(name="<:loses:853633469070835712> Losses", value=(res['user']['losses']), inline=True)
                        wl = "{:.2f}".format(win/lost)
                        page1.add_field(name="<a:wl:855110803082313728> W/L", value=wl, inline=True)
                        page1.add_field(name="<a:wool:853628583535968286> Wool Destroys", value=(res['user']['wool_destroys']), inline=True)
                        page1.add_field(name="Last Online", value=(timeago.format(ms/1000.0, now, 'en')), inline=True)
                        page1.add_field(name="Join Date", value=(timeago.format(ms2/1000.0, now, 'en')), inline=True)
                        page1.timestamp = datetime.datetime.utcnow()
                        page1.set_footer(text='Bot Created by ksndq#8052', icon_url="https://cdn.discordapp.com/avatars/431703739913732097/013868d08ceb35bf90fb568bfbd1e854.png?size=64")
                        page1.set_image(url='https://crafatar.com/renders/head/' + skin)
                        ################################################################
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get('https://tgmapi.cylonemc.net/mc/match/latest/' + mc_name, ) as r:
                            res = await r.json()
                            ms3 = res[0]['match']['startedDate']
                            i=0
                            page2 = discord.Embed(title="", color=0xbc2a82)
                            page2.set_author(name=mc_name + " Latest Match Stats")
                            page2.add_field(name="<a:wool:853628583535968286> Winning Team", value=(res[0]["match"]["winningTeam"].capitalize()), inline=False)
                            page2.add_field(name="<a:match:854808917024309328> Match Size", value=(res[0]["matchSize"]), inline=False)
                            page2.add_field(name="<:maps:853637839064924170> Map", value=(res[0]["loadedMap"]["name"]), inline=False)
                            page2.add_field(name="<a:clock:854800563857784872> Time elapsed", value=(res[0]["timeElapsed"]), inline=True)
                            page2.add_field(name="Started", value=(datetime.datetime.fromtimestamp(ms3/1000.0).strftime('%m-%d • %H:%M:%S')), inline=True)
                            page2.timestamp = datetime.datetime.utcnow()
                            page2.set_footer(text='Bot Created by ksndq#8052', icon_url="https://cdn.discordapp.com/avatars/431703739913732097/013868d08ceb35bf90fb568bfbd1e854.png?size=64")
                            page2.set_image(url='https://crafatar.com/renders/head/' + skin)
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
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed = pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '▶':
            if i < 2:
                i += 1
                await message.edit(embed = pages[i])
        elif str(reaction) == '⏭':
            i = 2
            await message.edit(embed = pages[i])
        
        try:
            reaction, user = await client.wait_for('reaction_add', timeout = 30.0, check = check)
            await message.remove_reaction(reaction, user)
        except:
            break

    await message.clear_reactions()

@stats.error
async def stats(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embedVar = discord.Embed(title=f"Command still on cooldown, try again in {error.retry_after:.2f} seconds!", color=0xFF0000)
        await ctx.send(embed=embedVar, delete_after=3.0)
        time.sleep(2)
        await ctx.message.delete()
        time.sleep(2)
    else:
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embedVar = discord.Embed(title=f"Please provide a player!", color=0xFF0000)
            await ctx.send(embed=embedVar, delete_after=4.0)
            time.sleep(2)
            await ctx.message.delete()
            time.sleep(2)
            pass

@client.command()
async def ping(ctx):
    if ctx.channel.id == 852546541830012988:
        await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')

client.run(config["bot"]["token"], reconnect=True)
