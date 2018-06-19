import discord
import json
import random
import datetime
import asyncio
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
import pytz
from discord.ext import commands
from __main__ import settings

class pokemon:
    """Pokemon cog"""

    def __init__(self, bot):
        self.bot = bot

    def save_data(self, data):
        with open('data/raidcog/raids.json', 'w') as outfile:
            json.dump(data, outfile)

    def get_user(self, user_id):
        return discord.User(id=str(user_id))

    @commands.group(pass_context=True, name='pokemon')
    async def _pokemon(self, context):
        """Raid Commands!"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Pokemon generator**\n'
            description = '**Commands**\n\n'
            description += '``{0}pokemon create``: Creates a new pokemon.\n'
            description += '\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_pokemon.command(pass_context=True, name='create')
    async def _create(self, context):
        with open('data/pokemon/pokemon.json') as rawPokemon:
            pokemonData = json.load(rawPokemon)
            pokemon = pokemonData[random.randint(1, 150) - 1]
        # with open('data/pokemon/moves.json') as rawMoves:
        #     movesData = json.load(rawMoves)
        pokemonMoveMax = len(pokemon["moves"]) - 1

        pokemon["learnedMoves"] = [
            pokemon["moves"][random.randint(0, pokemonMoveMax)],
            pokemon["moves"][random.randint(0, pokemonMoveMax)],
            pokemon["moves"][random.randint(0, pokemonMoveMax)],
            pokemon["moves"][random.randint(0, pokemonMoveMax)]
        ]

        pokemon["level"] = random.randint(1, 100)

        title = "Oh wow you caught a " + pokemon["name"] + " (" + pokemon["id"] + ")"
        description = "It's level " + pokemon["level"] + "\n"
        description += "It knows " + pokemon["learnedMoves"][0]["name"] + ",\n"
        description += pokemon["learnedMoves"][1]["name"] + ",\n"
        description += pokemon["learnedMoves"][2]["name"] + ",\n"
        description += "and " + pokemon["learnedMoves"][3]["name"] + ",\n"

        em = discord.Embed(title=title, description=description, color=discord.Color.blue())
        await self.bot.say(embed=em)



def setup(bot):
    bot.add_cog(pokemon(bot))
