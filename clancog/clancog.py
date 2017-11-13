import discord
from discord.ext import commands

class clancog:
    """Thunderdoges D2 clan link!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clan(self):
        """Thunderdoges D2 clan link!"""

        #Your code will go here
        await self.bot.say("https://www.bungie.net/en/ClanV2/Chat?groupId=2762856")

    @commands.command(pass_context=True)
    async def squad(self, context):
        """Thunderdoges D2 clan banner!"""

        #Your code will go here
        await self.bot.send_file(context.message.channel, 'data/clancog/raid.png')

def setup(bot):
    bot.add_cog(clancog(bot))