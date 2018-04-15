import pathlib
import asyncio  # noqa: F401
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from datetime import datetime

path = 'data/stolenparrot'

class stolenparrot:
    """Waterfall Convo Repeat and Join"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stolenparrot", pass_context=True)
    async def stolenparrot(self,ctx):
        """ask question , regurgitate answer """
        author = ctx.message.author
        author_channel = ctx.message.channel

        await self.bot.send_message("Please respond to this message")

        reply = await self.bot.wait_for_message(timeout=30, author=author, channel=author_channel)

        if reply is None:
            await self.bot.send_message("Okay, fine.")
        else:
            await self.bot.send_message(" ur a prankst er :" + reply.content)

def setup(bot):
    bot.add_cog(stolenparrot(bot))
