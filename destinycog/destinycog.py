import discord
import pycurl
import json
import re
import aiohttp
from io import BytesIO
from discord.ext import commands

class destinycog:
    """D2 api hook"""
    def __init__(self, bot):
        self.bot = bot
        self.apiKey = "72f9cb7bc66049cf81f4764358ad4e85"
        self.header = {
            'X-API-Key': self.apiKey
        }
        self.baseUrl = 'https://www.bungie.net/Platform'
        self.headers = {}

    def _header_function(self, header_line):
        # HTTP standard specifies that headers are encoded in iso-8859-1.
        # On Python 2, decoding step can be skipped.
        # On Python 3, decoding step is required.
        headerline = header_line.decode('iso-8859-1')

        # Header lines include the first status line (HTTP/1.x ...).
        # We are going to ignore all lines that don't have a colon in them.
        # This will botch headers that are split on multiple lines...
        if ':' not in headerline:
            return

        # Break the header line into header name and value.
        name, value = headerline.split(':', 1)

        # Remove whitespace that may be present.
        # Header lines include the trailing newline, and there may be whitespace
        # around the colon.
        name = name.strip()
        value = value.strip()

        # Header names are case insensitive.
        # Lowercase name here.
        name = name.lower()

        # Now we can actually record the header name and value.
        self.headers[name] = value

    @commands.group(pass_context=True, name='d')
    async def _d(self, context):
        """Destiny 2 API"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Destiny 2 API Utility**\n'
            description = '**Commands**\n\n'
            description += '``{0}users <user>``: Retrieves list of users.\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_d.command(pass_context=True, name='fusers')
    async def _fusers(self, context, q: str):
        with open('data/destinycog/dump', 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, self.baseUrl + '/User/SearchUsers/?q=' + q)
            c.setopt(c.HTTPHEADER, [
                'X-API-Key: ' + self.apiKey
            ])
            c.setopt(c.WRITEDATA, f)
            c.setopt(c.VERBOSE, True)
            c.perform()
            c.close()
        # Body is a byte string.
        # We have to know the encoding in order to print it to a text file
        # such as standard output.
        try:
            await self.bot.say("Successful :D")
        except discord.errors.HTTPException:
            await self.bot.say("404 Error :(")

    @_d.command(pass_context=True, name='users')
    async def _users(self, context, q: str):
        url = self.baseUrl + '/User/SearchUsers/?q=' + q
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(url) as resp:
                results = await resp.json()

        if 'error' in results:
            await self.bot.say("Couldn't search, something went wrong")
            return
        await self.bot.say(str(results))
        # self.headers = {}
        # buffer = BytesIO()
        # c = pycurl.Curl()
        # c.setopt(c.URL, self.baseUrl + '/User/SearchUsers/?q=' + q)
        # c.setopt(c.HTTPHEADER, [
        # ])
        # c.setopt(c.WRITEFUNCTION, buffer.write)
        # c.setopt(c.VERBOSE, True)
        # c.setopt(c.HEADERFUNCTION, self._header_function)
        # c.perform()
        # c.close()
        #
        # body = buffer.getvalue()
        #
        # encoding = None
        # if 'content-type' in self.headers:
        #     content_type = self.headers['content-type'].lower()
        #     match = re.search('charset=(\S+)', content_type)
        #     if match:
        #         encoding = match.group(1)
        #         print('Decoding using %s' % encoding)
        # if encoding is None:
        #     # Default encoding for HTML is iso-8859-1.
        #     # Other content types may have different default encoding,
        #     # or in case of binary data, may have no encoding at all.
        #     encoding = 'iso-8859-1'
        #     print('Assuming encoding is %s' % encoding)
        # output = body.decode(encoding)
        # # Body is a byte string.
        # # We have to know the encoding in order to print it to a text file
        # # such as standard output.
        # try:
        #     await self.bot.say(output)
        # except discord.errors.HTTPException:
        #     await self.bot.say("404 Error :(")


def setup(bot):
    bot.add_cog(destinycog(bot))