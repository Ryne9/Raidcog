import discord
import json
import random
import math
from PIL import Image
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
        self.background = Image.open('data/pokemon/sprites/battlebackground.png')
        self.background2 = Image.open('data/pokemon/sprites/background.png')
        self.playerbar = Image.open('data/pokemon/sprites/playerbar.png')
        self.enemybar = Image.open('data/pokemon/sprites/enemybar.png')
        with open('data/pokemon/pokemon.json') as rawPokemon:
            self.pokemonData = json.load(rawPokemon)
        with open('data/pokemon/moves.json') as rawMoves:
            self.moveData = json.load(rawMoves)

    # def save_data(self, data):
    #     with open('data/raidcog/raids.json', 'w') as outfile:
    #         json.dump(data, outfile)

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

    @_pokemon.command(pass_context=True, name='image')
    async def _image(self, context):
        pokemon1 = self.pokemonData[random.randint(1, 150) - 1]
        pokemon2 = self.pokemonData[random.randint(1, 150) - 1]
        image1 = Image.open('data/pokemon/sprites/' + str(pokemon1["id"]) + 'b.png').convert("RGBA")
        image1 = image1.resize(size=(96 * 2, 96 * 2))
        image2 = Image.open('data/pokemon/sprites/' + str(pokemon2["id"]) + 'f.png').convert("RGBA")
        background = self.background.copy()
        background.paste(image2, (165, 5), image2)
        background.paste(image1, (10, int(200 - 96 * 1.75)), image1)
        background = background.resize(size=(256 * 2, 192 * 2))
        background.save("data/pokemon/compost.png", quality=100)
        await self.bot.send_file(context.message.channel, 'data/pokemon/compost.png')

    @_pokemon.command(pass_context=True, name='battle')
    async def _battle(self, context):
        pokemon1 = self.pokemonData[random.randint(1, 150) - 1]
        pokemon2 = self.pokemonData[random.randint(1, 150) - 1]
        image1 = Image.open('data/pokemon/sprites/' + str(pokemon1["id"]) + 'b.png').convert("RGBA")
        image1 = image1.resize(size=(96 * 2, 96 * 2))
        image2 = Image.open('data/pokemon/sprites/' + str(pokemon2["id"]) + 'f.png').convert("RGBA")
        background = self.background2.copy()
        background.paste(image2, (148, 15), image2)
        background.paste(image1, (-20, int(200 - 96 * 1.75)), image1)
        background.paste(self.enemybar, (5, 23), self.enemybar)
        background.paste(self.playerbar, (142, 95), self.playerbar)
        background = background.resize(size=(255 * 2, 143 * 2))
        background.save("data/compost.png", quality=100)
        await self.bot.send_file(context.message.channel, 'data/pokemon/compost.png')

    @_pokemon.command(pass_context=True, name='create')
    async def _create(self, context):
        pokemon = self.pokemonData[random.randint(1, 150) - 1]
        pokemonMoveMax = len(pokemon["moves"]) - 1

        pokemon["learnedMoves"] = [
            pokemon["moves"][random.randint(0, pokemonMoveMax)],
            pokemon["moves"][random.randint(0, pokemonMoveMax)],
            pokemon["moves"][random.randint(0, pokemonMoveMax)],
            pokemon["moves"][random.randint(0, pokemonMoveMax)]
        ]

        pokemon["level"] = random.randint(1, 100)
        pokemon["actualStats"] = self.calculate_stats(pokemon["stats"], pokemon["level"])

        title = "Oh wow you caught a " + pokemon["name"] + "!"
        description = "PokeDex Number: " + str(pokemon["id"]) + "\n"
        description += "Height: " + str(pokemon["height"])
        description += " Weight: " + str(pokemon["weight"]) + "\n"
        description += "Level: " + str(pokemon["level"]) + "\n"
        description += "It knows " + pokemon["learnedMoves"][0]["name"] + ", "
        description += pokemon["learnedMoves"][1]["name"] + ", "
        description += pokemon["learnedMoves"][2]["name"] + ", "
        description += "and " + pokemon["learnedMoves"][3]["name"] + "!\n"
        description += "Actual Stats:\n"
        description += "Speed: " + str(pokemon["actualStats"]["speed"]) + " HP: " + str(
            pokemon["actualStats"]["hp"]) + "\n"
        description += "Attack: " + str(pokemon["actualStats"]["attack"]) + " Special Attack: " + str(
            pokemon["actualStats"]["special-attack"]) + "\n"
        description += "Defense: " + str(pokemon["actualStats"]["defense"]) + " Special Defense: " + str(
            pokemon["actualStats"]["special-defense"]) + "\n"

        em = discord.Embed(title=title, description=description, color=discord.Color.blue())
        em.set_image(url=pokemon["sprites"]["front_default"])
        await self.bot.say(embed=em)

    def calculate_stats(self, stats, level):
        return {
            "hp": self.calc_hp(stats["hp"]["base"], level),
            "attack": self.calc_stat(stats["attack"]["base"], level),
            "special-attack": self.calc_stat(stats["special-attack"]["base"], level),
            "defense": self.calc_stat(stats["defense"]["base"], level),
            "special-defense": self.calc_stat(stats["special-defense"]["base"], level),
            "speed": self.calc_stat(stats["speed"]["base"], level)
        }

    def calc_hp(self, hp, level):
        return math.floor((2 * hp) * level / 100) + level + 10

    def calc_stat(self, stat, level):
        return math.floor((2 * stat * level) / 100) + 5

def setup(bot):
    bot.add_cog(pokemon(bot))
