import discord
import json
import datetime
from discord.ext import commands

class raidcog:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot

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
    async def _list(self):
        #Your code will go here
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            title = "Current raids:\n"
            description = ""
            for raid in data:
                description += "**" + raid['title'] + "** [" + str(raid['id']) + "]\n"
                description += raid['date'] + "\n"
                for members in raid['members']:
                    description += " - " + members['name'] + "\n"
                description += "\n"

            em = discord.Embed(title=title, description=description, color=discord.Color.blue())
            em.set_footer(text='all of these raids are fake don\'t join them')

            await self.bot.say(embed=em)

    @_raid.command(pass_context=True, name='create')
    async def _create(self, context, title, date, time):
        #Your code will go here
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
                'date': str(dt)
            }
            data.append(newRaid)
        self.save_data(data)
        await self.bot.say("Added your raid " + title + " for " + str(dt) + ".")

    @_raid.command(pass_context=True, name='join')
    async def _join(self, context, id: int):
        # Your code will go here
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

def setup(bot):
    bot.add_cog(raidcog(bot))
