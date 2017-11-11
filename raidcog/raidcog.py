import discord
import json
from discord.ext import commands

class raidcog:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def raid(self):
        """This does stuff!"""

        #Your code will go here
        with open('data\\raids.json') as data_file:
            data = json.load(data_file)
        await self.bot.say(data['title'])

def setup(bot):
    bot.add_cog(raidcog(bot))
