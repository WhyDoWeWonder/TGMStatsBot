import discord
import aiohttp

from datetime import datetime
import datetime

from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from structs.proxy import ProxyConnectorWrapper
from structs.global_vars import GlobalVariables


async def process_leaderboard_command(self, ctx):
    if ctx.channel.id in self.global_variables.config['bot']['channels']:
        connector = ProxyConnectorWrapper().connector
        async with aiohttp.ClientSession(connector=connector) as cs:
            stat_types = ['kills', 'wins', 'xp', 'losses']
            pages = []
            for i in range(0, len(stat_types)):
                async with cs.get('https://api.pvparca.de/mc/leaderboard/' + stat_types[i]) as r:
                    # currently not very efficient since we check if the API is down however many stat types we
                    # have, though it is possible for the API to go down as we request the second or 3rd stat
                    # type it's incredibly unlikely, not sure if this repeated checking is worth it
                    if r.status == 522 or r.status == 502:
                        error_message = "The PVP Arcade Team Games API is currently down, please wait for it to by " \
                                        "restored to get up-to-date statistics."
                        print(error_message)
                        embed_var = discord.Embed(title=error_message, color=0xFF0000)
                        await ctx.send(embed=embed_var)
                        # Add a cache that returns cached values if the API is down with the date of when the
                        # data Was last updated
                        return
                    res = await r.json(content_type=None)

                    pages.append(self.create_embed(res, i + 1, stat_types[i]))

            message = await ctx.send(embed=pages[0])
            await message.add_reaction('◀')
            await message.add_reaction('▶')
            self.global_variables.messages.append(
                {"message": message, "author": ctx.author, "pages": pages, "page_number": 0})

    else:
        embed_var = discord.Embed(title="You can't use that here!", color=0xFF0000)
        await ctx.send(embed=embed_var, delete_after=5.0)


class Leaderboard(commands.Cog):
    config = GlobalVariables().config
    guild_ids = config['bot']['guilds']

    def __init__(self, client):
        self.client = client
        self.leaderboard_prefix = {0: self.config['emoji']['first_place'],
                                   1: self.config['emoji']['second_place'],
                                   2: self.config['emoji']['third_place']}

    def create_embed(self, res, page_number: int, leaderboard_type: str):
        #######
        #######
        if leaderboard_type == "xp":
            leaderboard_type = "level"

        page = discord.Embed(title="", color=0xbc2a82)
        page.set_author(name="PVP Arcade Team Games " + leaderboard_type.title() + " Leaderboard " +
                             str(page_number) + "/4")

        for i in range(0, 10):
            leaderboard_prefix = self.leaderboard_prefix.get(i, "")
            page.add_field(name=leaderboard_prefix + " " + str(i + 1) + ". " + res[i]['name'],
                           value=res[i][leaderboard_type], inline=False)

        page.timestamp = datetime.datetime.utcnow()
        page.set_footer(text='Bot Created by ksndq and LordofLightning',
                        icon_url=self.config['bot']['icon_url'])
        ################################################################
        return page

    @commands.command(aliases=["lb", "leaderboards"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self, ctx: commands.context):
        async with ctx.typing():
            await process_leaderboard_command(self, ctx)

    @cog_ext.cog_slash(name='Leaderboard', description='Displays team games leaderboards', guild_ids=guild_ids)
    async def _leaderboard(self, ctx: SlashContext):
        await ctx.defer()
        await process_leaderboard_command(self, ctx)


def setup(client):
    client.add_cog(Leaderboard(client))
