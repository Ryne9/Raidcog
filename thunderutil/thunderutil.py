import discord
import json
import datetime
import asyncio
from discord.ext import commands

class thunderutil:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot
        self.notification_task = bot.loop.create_task(self.spam())

    @commands.group(pass_context=True, name='tu')
    async def _tu(self, context):
        """Thunderdoges Utilities"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Welcome to Thunderdoge\'s Utility.**\n'
            description = '**Commands**\n\n'
            description += '``{0}gc``: Retrieves channel by ID.\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @tu.command(pass_context=True, name='gc')
    async def _get_channel(self, context, id: int):
        object = discord.Server.get_channel(id)
        await self.bot.say("Name: " + object.name + "\nID:" + str(object.id))


def setup(bot):
    bot.add_cog(thunderutil(bot))