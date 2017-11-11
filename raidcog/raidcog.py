import discord
import json
import datetime
import asyncio
from pytz import timezone
import pytz
from discord.ext import commands

class raidcog:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot
        self.notification_task = bot.loop.create_task(self.spam())
        self.channel = ""
        self.fmt = "%b %d, %Y %I:%M"
        self.timezones = {
            "EST": timezone('US/Eastern'),
            "E": timezone('US/Eastern'),
            "PST": timezone('US/Pacific-New'),
            "P": timezone('US/Pacific-New')
        }

    def save_data(self, data):
        with open('data/raidcog/raids.json', 'w') as outfile:
            json.dump(data, outfile)

    @commands.group(pass_context=True, name='raid')
    async def _raid(self, context):
        """Raid Commands!"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Welcome to Thunderdoge\'s raid manager.**\n'
            description = '**Commands**\n\n'
            description += '``{0}list``: Displays all raids, active and upcoming.\n'
            description += '``{0}create``: Creates a new raid.\n'
            description += '``{0}join``: Joins a raid.\n'
            description += '``{0}delete``: Deletes a raid you created.\n'

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

    @_raid.command(pass_context=True, name='create')
    async def _create(self, context, title, date, time, timezone: str):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            dt = datetime.datetime.strptime(date + time, '%m/%d/%y%I:%M%p')
            newRaid = {
                'members': [{
                    'id':context.message.author.id,
                    'name':context.message.author.name
                }],
                'id': len(data),
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

def setup(bot):
    bot.add_cog(raidcog(bot))
