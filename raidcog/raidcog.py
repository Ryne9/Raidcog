import discord
import json
import datetime
import asyncio
from cogs.utils.dataIO import dataIO
from pytz import timezone
from cogs.utils import checks
import pytz
from discord.ext import commands
from __main__ import settings

class raidcog:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot
        self.fmt = "%b %d, %Y %I:%M%p"

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
            description += '``{0}raid delete #``: Deletes a raid you created.\n'
            description += '``{0}raid remove #``: Removes a raid you created.\n'
            description += '``{0}raid join #``: Joins a raid.\n'
            description += '``{0}raid leave #``: Leaves a raid.\n'
            description += '``{0}raid list <filter>``: Displays all raids, optionally can filter by a keyword.\n'
            description += '``{0}raid clear``: Removes all raids. (Admin only)\n'
            description += '\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_raid.command(pass_context=True, name='list')
    async def _list(self, context, filter: str = None):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            title = "Current raids:\n"
            description = ""
            for raid in data:
                if (filter and filter.upper() in raid['title'].upper()) or not filter:
                    date = datetime.datetime.strptime(raid['date'], '%Y-%m-%d %H:%M:%S')
                    description += "__**" + raid['title'] + "**__ [" + str(raid['id']) + "]\n"
                    description += str(date.strftime(self.fmt)) + " " + raid['timezone'] + "\n"
                    for members in raid['members']:
                        role = ""
                        if 'role' in members.keys():
                            role = "[{}]".format(members['role'])
                        if members['id'] == raid['members'][0]['id']:
                            description += " - " + members['name'] + " " + role + " (Raid Leader)\n"
                        else:
                            description += " - " + members['name'] + " " + role + "\n"
                    description += "\n"
            em = discord.Embed(title=title, description=description, color=discord.Color.blue())
            em.set_footer(text='This was sent to ' + context.message.channel.name + " : " + str(context.message.channel.id))

            await self.bot.say(embed=em)

    @_raid.command(pass_context=True, name='tell')
    async def _tell(self, context, id: int):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            print("This is the id: " + str(id) + "\n")
            for raid in data:
                print("Checking raid: " + str(raid) + " " + str(raid["id"]) + "\n")
                if raid['id'] == id:
                    inRaid = False
                    for member in raid["members"]:
                        if member['id'] == context.message.author.id:
                            inRaid = True
                    if not inRaid:
                        await self.bot.say("You aren't in that raid, you potato.")
                        return
                    for member in raid['members']:
                        user = self.get_user(member['id'])
                        await self.bot.send_message(user, "Raid reminder: " + raid['title'] + " starts soon!")
                    await self.bot.say("ShibeBot has tracked down all members of the raid")
                    return
            await self.bot.say("Raid wasn't found :(")

    async def _failed_create(self, author):
        await self.bot.send_message(author,
                                    "Okay, try again later.")

    @_raid.command(pass_context=True, name='create')
    async def _create(self, context):
        author = context.message.author
        await self.bot.say("Check your DM to continue.")

        dm = await self.bot.send_message(author, "Please respond to continue setting up the raid.\n"
                                                 "What game is the raid for?\n"
                                                 "Ex: `WoW` or `Destiny`")
        game_msg = await self.bot.wait_for_message(channel=dm.channel,
                                                   author=author, timeout=30)

        if game_msg is None:
            self._failed_create(author)
            return

        game = game_msg.content

        dm = await self.bot.send_message(author,
                                         "Give a raid description."
                                         "Ex: `Prestige Argos` ; `WoW Mythics` ; `LFR`")

        desc_msg = await self.bot.wait_for_message(channel=dm.channel,
                                                   author=author, timeout=30)

        if desc_msg is None:
            self._failed_create(author)
            return

        desc = desc_msg.content

        dm = await self.bot.send_message(author,
                                         "Give a date for the raid. Follow the format: `MM/DD/YY` or 'MM/DD' "
                                         "Ex: `12/25/17` or `12/25`")

        date_msg = await self.bot.wait_for_message(channel=dm.channel,
                                                  author=author, timeout=30)
        if date_msg is None:
            self._failed_create(author)
            return

    # ---Date processing, data validation---
        in_date = date_msg.content
        today = datetime.datetime.today()

        if "/" not in in_date:
            await self.bot.send_message(author,
                                        "Check your date formatting, are you missing a `:`?")
            return

        date_bits = in_date.split('/')

        if not (len(date_bits) == 2 or len(date_bits) == 3):
            await self.bot.send_message(author,
                                        "Check your date formatting, did you make a typo?")

        if len(date_bits) == 2:
            date = in_date + "/" + datetime.datetime.strftime(today, '%y')
        else:
            date = in_date

        dm = await self.bot.send_message(author,
                                         "Give a time for the raid. Follow the format: `H:MA` or `HA` "
                                         "Ex: `8:00PM` or `11:00AM` or `8PM` or `11AM`")

        time_msg = await self.bot.wait_for_message(channel=dm.channel,
                                                   author=author, timeout=30)
        if time_msg is None:
            self._failed_create(author)
            return

    # ---Time processing and validation---
        in_time = time_msg.content

        if ":" not in in_time and len(in_time) not in [3, 4]:
            await self.bot.send_message(author,
                                        "Check your time formatting.")
            return

        # Assume time format is Hour:MinuteAM
        time_format = '%I:%M%p'

        time_bits = in_time.split(':')
        # Assume time format is HourAM
        if len(time_bits) == 1:
            time_format = '%I%p'

        dt = datetime.datetime.strptime(date + in_time, '%m/%d/%y' + time_format)

        dm = await self.bot.send_message(author,
                                         "Give the timezone for the raid."
                                         "Ex: `PST` , `EST` etc. ")

        timezone_msg = await self.bot.wait_for_message(channel=dm.channel,
                                                       author=author, timeout=30)
        if timezone_msg is None:
            self._failed_create(author)
            return

        timezone = time_msg.content

        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)

            finding = True
            id = 0
            title = game + " | " + desc
            while finding:
                finding = False
                for raid in data:
                    if raid['id'] == id:
                        id += 1
                        finding = True
                        break
            new_raid = {
                'members': [{
                    'id': author.id,
                    'name': author.name
                }],
                'id': id,
                'title': title,
                'date': str(dt),
                'timezone': timezone
            }
            data.append(new_raid)
        self.save_data(data)
        await self.bot.send_message(author,
                                    "Added your raid " + title + " for " + str(dt) + ".")

    @_raid.command(pass_context=True, name='join')
    async def _join(self, context, id: int, role: str = None):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for raid in data:
                if raid['id'] == id:
                    for member in raid['members']:
                        if member['id'] == context.message.author.id:
                            await self.bot.say("You are already in this raid.")
                            return
                    if role:
                        raid['members'].append({
                            'id': context.message.author.id,
                            'name': context.message.author.name,
                            'role': role
                        })
                    else:
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
        await self._remove_raid(context, id)

    @_raid.command(pass_context=True, name='remove')
    async def _remove(self, context, id: int):
        await self._remove_raid(context, id)

    async def _remove_raid(self, context, id: int):
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            for raid in data:
                if raid['id'] == id:
                    authorId = context.message.author.id
                    if raid['members'][0]['id'] == authorId or settings.owner == authorId or authorId in context.bot.settings.co_owners:
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

def check_files():
    f = "data/raidcog/raids.json"
    if not dataIO.is_valid_json(f):
        print("Creating default raids's settings.json...")
        dataIO.save_json(f, [])

def setup(bot):
    check_files()
    bot.add_cog(raidcog(bot))
