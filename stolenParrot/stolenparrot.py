import pathlib
import asyncio  # noqa: F401
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from datetime import datetime

path = 'data/parrot'

class parrot:
    """Waterfall Convo Repeat and Join"""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="stolenparrot", pass_context=True)
    async def parrot(self,ctx):
        """ask question , regurgitate answer """
        author = ctx.message.author
        await self.bot.send_message("Please respond to this message")

        reply = await self.bot.wait_for_message(author=author, timeout=30)
        if reply is None:
            await self.bot.send_message(author,
                                        "Okay, fine.")
        else:
            self.bot.send_message(author, ":", reply)

def setup(bot):
    bot.add_cog(parrot(bot))