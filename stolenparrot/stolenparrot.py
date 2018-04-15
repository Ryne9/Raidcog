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
        author_channel = ctx.message.channel

        await self.bot.send_message(author_channel, "hey u pls repond to me")

        await self.uwot(ctx)

    async def uwot(self, ctx):
        author = ctx.message.author
        author_channel = ctx.message.channel

        reply = await self.bot.wait_for_message(timeout=30, author=author, channel=author_channel)

        if reply is None:
            await self.bot.send_message(author_channel, "Okay, fine.")
        elif reply.content == "stop":
            await self.bot.send_message(author_channel, " omg fine wtf")
        else:
            await self.bot.send_message(author_channel, " ur a prankst er :" + reply.content)
            await self.uwot(ctx)

def setup(bot):
    bot.add_cog(stolenparrot(bot))
