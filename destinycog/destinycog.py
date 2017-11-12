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

    def save_data(self, data):
        with open('data/destinycog/users.json', 'w') as outfile:
            json.dump(data, outfile)

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
                print(results)
                output = ""
                for user in results['Response']:
                    if 'psnDisplayName' in user.keys():
                        psn = "\n - psn: " + user['psnDisplayName']
                    else:
                        psn = ""

                    if 'blizzardDisplayName' in user.keys():
                        bnet = "\n - bnet: " + user['blizzardDisplayName']
                    else:
                        bnet = ""
                    output += "**" + user['displayName'] + "**" + bnet + psn + "\n"

        if 'error' in results:
            await self.bot.say("Couldn't search, something went wrong")
            return
        try:
            await self.bot.say(str(output))
        except discord.errors.HTTPException:
            await self.bot.say("Oops it broke :(")

    @_d.command(pass_context=True, name='membershipId')
    async def _membership_id(self, context, q: str):
        url = self.baseUrl + '/User/SearchUsers/?q=' + q
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(url) as resp:
                results = await resp.json()
                print(results)
                output = ""
                for user in results['Response']:
                    if 'blizzardDisplayName' in user.keys():
                        bnet = "\n - bnet: " + user['blizzardDisplayName']
                    else:
                        bnet = ""
                    output += "**" + user['displayName'] + "**" + bnet + "\n - memId: " + user['membershipId'] + "\n"

        if 'error' in results:
            await self.bot.say("Couldn't search, something went wrong")
            return
        try:
            await self.bot.say(str(output))
        except discord.errors.HTTPException:
            await self.bot.say("Oops it broke :(")

    @_d.command(pass_context=True, name='registerId')
    async def _register_id(self, context, q: str):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for user in data:
                if user['id'] == context.message.author.id:
                    user['membershipId'] = q
                    self.save_data(data)
                    return
            user = {
                "id": context.message.author.id,
                "membershipId": q
            }
            data.append(user)
            self.save_data(data)

    @_d.command(pass_context=True, name='groups')
    async def _groups(self, context, q: str):
        url = self.baseUrl + ' /GroupV2/Search/'
        payload = {"name": q,
                   "groupType": "Clan",
                   "localeFilter": "en",
                   "creationDate": "All",
                   "sortBy": "Name",
                   "type": "Search",
                   "tagText": q,
                   "itemsPerPage": 10,
                   "currentPage": 1,
                   "requestContinuationToken":"false"}
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.post(url,
                                    data=json.dumps(payload)) as resp:
                results = await resp.json()
                print(results)
                output = "????"

        if 'error' in results:
            await self.bot.say("Couldn't search, something went wrong")
            return
        try:
            await self.bot.say(str(output))
        except discord.errors.HTTPException:
            await self.bot.say("Oops it broke :(")

def setup(bot):
    bot.add_cog(destinycog(bot))