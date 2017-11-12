import discord
import pycurl
from io import BytesIO
from discord.ext import commands

class thunderutil:
    """D2 api hook"""

    def __init__(self, bot):
        self.bot = bot
        self.apiKey = "72f9cb7bc66049cf81f4764358ad4e85"

    @commands.group(pass_context=True, name='d')
    async def _d(self, context):
        """Destiny 2 API"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Destiny 2 API Utility**\n'
            description = '**Commands**\n\n'
            description += '``{0}gc``: Retrieves channel by ID.\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_d.command(pass_context=True, name='users')
    async def _get_channel(self, context, q: str):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://www.bungie.net/Platform/User/SearchUsers/?q=' + q)
        c.setopt(c.HTTPHEADER, [
            'X-API-Key: ' + self.apiKey
        ])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        body = buffer.getvalue()
        decodedBody = str(body.decode('iso-8859-1'))
        # Body is a byte string.
        # We have to know the encoding in order to print it to a text file
        # such as standard output.
        try:
            await self.bot.say(decodedBody)
        except discord.errors.HTTPException:
            await self.bot.say("404 Error :(")


def setup(bot):
    bot.add_cog(thunderutil(bot))