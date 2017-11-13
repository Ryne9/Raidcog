import discord
import json
import datetime
import asyncio
from cogs.utils.dataIO import dataIO
from pytz import timezone
from cogs.utils import checks
import pytz
from discord.ext import commands

class raidcog:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot
        self.notification_task = bot.loop.create_task(self.spam())
        self.channel = ""
        self.fmt = "%b %d, %Y %I:%M%p"
        self.timezones = {
            "EST": timezone('US/Eastern'),
            "E": timezone('US/Eastern'),
            "PST": timezone('US/Pacific-New'),
            "P": timezone('US/Pacific-New')
        }

    def save_data(self, data):
        with open('data/raidcog/raids.json', 'w') as outfile:
            json.dump(data, outfile)

    def get_user(self, user_id):
        return discord.User(id=str(user_id))

    @commands.group(pass_context=True, name='raid')
    async def _raid(self, context):
        """Raid Commands!"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Welcome to Thunderdoge\'s raid manager.**\n'
            description = '**Commands**\n\n'
            description += '``{0}raid create``: Creates a new raid.\n'
            description += '``{0}raid delete``: Deletes a raid you created.\n'
            description += '``{0}raid join #``: Joins a raid.\n'
            description += '``{0}raid leave``: Leaves a raid.\n'
            description += '``{0}raid list``: Displays all raids, active and upcoming.\n'
            description += '\n'
            description += 'Example: ``.raid create "THE RAID" 12/25/17 8:00pm PST``\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_raid.command(pass_context=True, name='list')
    async def _list(self, context):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            title = "Current raids:\n"
            description = ""
            for raid in data:
                date = datetime.datetime.strptime(raid['date'], '%Y-%m-%d %H:%M:%S')
                description += "__**" + raid['title'] + "**__ [" + str(raid['id']) + "]\n"
                description += str(date.strftime(self.fmt)) + " " + raid['timezone'] + "\n"
                for members in raid['members']:
                    if members['id'] == raid['members'][0]['id']:
                        description += " - " + members['name'] + " (Raid Leader)\n"
                    else:
                        description += " - " + members['name'] + "\n"
                description += "\n"

            em = discord.Embed(title=title, description=description, color=discord.Color.blue())
            em.set_footer(text='This was sent to ' + context.message.channel.name + " : " + str(context.message.channel.id))

            await self.bot.say(embed=em)

    @_raid.command(pass_context=True, name='tell')
    async def _tell(self, context, id):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for raid in data:
                if raid["id"] == str(id):
                    for member in raid['members']:
                        user = self.get_user(member['id'])
                        await self.bot.send_message(user, "Raid reminder: " + raid['title'] + " starts soon!")
            await self.bot.say("Raid wasn't found :(")


    @_raid.command(pass_context=True, name='create')
    async def _create(self, context, title, inDate, inTime, timezone: str):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            today = datetime.datetime.today()
            timeFormat = '%I:%M%p'

            dateBits = inDate.split('/')
            if len(dateBits) == 2:
                date = inDate + "/" + datetime.datetime.strftime(today, '%y')
            else:
                date = inDate

            timeBits = inTime.split(':')
            if len(timeBits) == 1:
                timeFormat = '%I%p'

            dt = datetime.datetime.strptime(date + inTime, '%m/%d/%y' + timeFormat)
            finding = True
            id = len(data)
            while finding:
                finding = False
                for raid in data:
                    if raid['id'] == id:
                        id += 1
                        finding = True
                        break
            newRaid = {
                'members': [{
                    'id':context.message.author.id,
                    'name':context.message.author.name
                }],
                'id': id,
                'title': title,
                'date': str(dt),
                'timezone': timezone
            }
            data.append(newRaid)
        self.save_data(data)
        await self.bot.say("Added your raid " + title + " for " + str(dt) + ".")

    @_raid.command(pass_context=True, name='join')
    async def _join(self, context, id: int):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for raid in data:
                if raid['id'] == id:
                    for member in raid['members']:
                        if member['id'] == context.message.author.id:
                            await self.bot.say("You are already in this raid.")
                            return
                    raid['members'].append({
                        'id': context.message.author.id,
                        'name': context.message.author.name
                    })
                    self.save_data(data)
                    await self.bot.say("Joined raid " + raid['title'])
                    return
        await self.bot.say("Couldn't find raid to join with ID " + str(id))

    @_raid.command(pass_context=True, name='leave')
    async def _leave(self, context, id: int):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for raid in data:
                if raid['id'] == id:
                    for member in raid['members']:
                        if member['id'] == context.message.author.id:
                            raid['members'] = [d for d in raid['members'] if d.get('id') != context.message.author.id]
                            await self.bot.say("You left raid " + str(id) + ".")
                            if len(raid['members']) == 0:
                                data.remove(raid)
                            self.save_data(data)
                            return
        await self.bot.say("You weren't in raid " + str(id) + ".")

    @_raid.command(pass_context=True, name='delete')
    async def _delete(self, context, id: int):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for raid in data:
                if raid['id'] == id:
                    if raid['members'][0]['id'] == context.message.author.id:
                        data.remove(raid)
                        self.save_data(data)
                        await self.bot.say("Removed the raid.")
                    else:
                        await self.bot.say("You are not the creator of this raid.")

    @_raid.command(pass_context=True, name='clear')
    @checks.is_owner()
    async def _clear(self):
        data = []
        self.save_data(data)
        await self.bot.say("Cleared all raids.")

    @_raid.command(pass_context=True, name='spamhere')
    async def _spamhere(self, context):
        self.channel = context.message.channel

    async def _send_message(self, channel, message):
        em = discord.Embed(description=message, color=discord.Color.green())
        await self.bot.send_message(channel, embed=em)

    async def spam(self):
        while 'raidcog' in self.bot.cogs:
            await self._send_message(self.channel, "raidbot spam destroy")
            await asyncio.sleep(20)

    def __unload(self):
        self.notification_task.cancel()

def check_files():
    f = "data/raidcog/raids.json"
    if not dataIO.is_valid_json(f):
        print("Creating default raids's settings.json...")
        dataIO.save_json(f, [])

def setup(bot):
    check_files()
    bot.add_cog(raidcog(bot))
