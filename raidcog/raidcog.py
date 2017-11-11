import discord
import json
from discord.ext import commands

class raidcog:
    """Custom D2 raid cog for Thunderdoges"""

    def __init__(self, bot):
        self.bot = bot

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
                description += "**" + raid['title'] + "**\n"
                for members in raid['members']:
                    description += " - " + members + "\n"
                description += "*join this raid by using .raid join " + str(raid['id']) + "*\n"
                description += "\n"

            em = discord.Embed(title=title, description=description, color=discord.Color.blue())
            em.set_footer(text='all of these raids are fake don\'t join them')

            await self.bot.say(embed=em)

    @_raid.command(pass_context=True, name='create')
    async def _create(self, context, title):
        #Your code will go here
        with open('data/raidcog/raids.json') as data_file:
            data = json.load(data_file)
            newRaid = {
                'members': [context.message.author.name],
                'id': len(data),
                'title': title
            }
            data.append(newRaid)
        with open('data/raidcog/raids.json', 'w') as outfile:
                json.dump(data, outfile)

        await self.bot.say("Probably added your raid.")

def setup(bot):
    bot.add_cog(raidcog(bot))
