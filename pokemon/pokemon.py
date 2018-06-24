import discord
import json
import random
import math
from PIL import Image, ImageDraw, ImageFont
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
        self.backgrounds = [
            Image.open('data/pokemon/sprites/background.png'),
            # Image.open('data/pokemon/sprites/cavebackground.png'),
            # Image.open('data/pokemon/sprites/darkbackground.png'),
            # Image.open('data/pokemon/sprites/ghostbackground.png'),
            Image.open('data/pokemon/sprites/normalbackground.png'),
            Image.open('data/pokemon/sprites/rockbackground.png'),
            Image.open('data/pokemon/sprites/sandbackground.png'),
            Image.open('data/pokemon/sprites/snowbackground.png'),
            Image.open('data/pokemon/sprites/steelbackground.png'),
            Image.open('data/pokemon/sprites/waterbackground.png'),
        ]
        self.playerbar = Image.open('data/pokemon/sprites/playerbar.png')
        self.enemybar = Image.open('data/pokemon/sprites/enemybar.png')
        with open('data/pokemon/pokemon.json') as rawPokemon:
            self.pokemonData = json.load(rawPokemon)
        with open('data/pokemon/moves.json') as rawMoves:
            self.moveData = json.load(rawMoves)
        self.font = ImageFont.truetype('data/pokemon/pokemonname.ttf', 10)
        self.healthFont = ImageFont.truetype('data/pokemon/pokemonname.ttf', 9)
        self.healthbar_high = Image.open('data/pokemon/sprites/healthbar_high.png')
        self.healthbar_half = Image.open('data/pokemon/sprites/healthbar_half.png')
        self.healthbar_low = Image.open('data/pokemon/sprites/healthbar_low.png')

    def get_user(self, user_id):
        return discord.User(id=str(user_id))

    def getHealthBar(self, health, maxHealth):
        if (health > maxHealth / 2):
            healthbar = self.healthbar_high.copy()
        elif (health <= maxHealth / 2) and (health > maxHealth * 0.2):
            healthbar = self.healthbar_half.copy()
        else:
            healthbar = self.healthbar_low.copy()
        healthbar = healthbar.resize(size=(int((health/maxHealth) * 84), 5))
        return healthbar


    def makePlayerBar(self, pokemon):
        plyrbar = self.playerbar.copy()
        draw = ImageDraw.Draw(plyrbar)
        # Player pokemon name
        draw.text((6, -2), str.capitalize(pokemon["name"]), font=self.font, fill=(0, 0, 0, 255))
        # Player pokemon level
        draw.text((145, 0), str(pokemon["level"]), font=self.font, fill=(0, 0, 0, 255))
        # Player health
        health = pokemon["health"]
        leftPad = len(str(health))
        draw.text((131 - (10) * leftPad, 23), str(health), font=self.healthFont, fill=(255, 255, 255, 255))
        draw.text((140, 23), str(pokemon["actualStats"]["hp"]), font=self.healthFont, fill=(255, 255, 255, 255))
        healthbar = self.getHealthBar(pokemon["health"], pokemon["actualStats"]["hp"])
        plyrbar.paste(healthbar, (87, 16))
        return plyrbar

    def makeEnemyBar(self, pokemon):
        enmybr = self.enemybar.copy()
        draw = ImageDraw.Draw(enmybr)
        # Enemy pokmeon name
        draw.text((5, -1), str.capitalize(pokemon["name"]), font=self.font, fill=(0, 0, 0, 255))
        # Enemy pokmeon level
        draw.text((152, 0), str(pokemon["level"]), font=self.font, fill=(0, 0, 0, 255))
        healthbar = self.getHealthBar(pokemon["health"], pokemon["actualStats"]["hp"])
        enmybr.paste(healthbar, (66, 17))
        return enmybr

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
        background = self.backgrounds[random.randint(0, len(self.backgrounds) - 1)].copy()
        background.paste(image2, (165, 5), image2)
        background.paste(image1, (10, int(200 - 96 * 1.75)), image1)
        background = background.resize(size=(256 * 2, 192 * 2))
        background.save("data/pokemon/compost.png", quality=100)
        await self.bot.send_file(context.message.channel, 'data/pokemon/compost.png')

    @_pokemon.command(pass_context=True, name='battle')
    async def _battle(self, context, x: int, y: int):
        level = random.randint(1, 100)
        pokemon1 = self.pokemonData[random.randint(1, 150) - 1]
        pokemon2 = self.pokemonData[random.randint(1, 150) - 1]

        pokemon1["level"] = level
        pokemon2["level"] = level
        pokemon1["actualStats"] = self.calculate_stats(pokemon1["stats"], pokemon1["level"])
        pokemon2["actualStats"] = self.calculate_stats(pokemon2["stats"], pokemon2["level"])
        pokemon1["health"] = random.randint(1, pokemon1["actualStats"]["hp"])
        pokemon2["health"] = random.randint(1, pokemon2["actualStats"]["hp"])

        image1 = Image.open('data/pokemon/sprites/' + str(pokemon1["id"]) + 'b.png').convert("RGBA")
        image1 = image1.resize(size=(96 * 3, 96 * 3))
        image2 = Image.open('data/pokemon/sprites/' + str(pokemon2["id"]) + 'f.png').convert("RGBA")
        image2 = image2.resize(size=(144, 144))

        background = self.backgrounds[random.randint(0, len(self.backgrounds) - 1)].copy()
        background.paste(image2, (228, 60), image2)
        background.paste(image1, (-53, 57), image1)

        plyrbar = self.makePlayerBar(pokemon1)
        background.paste(plyrbar, (200, 188), plyrbar)
        enmybar = self.makeEnemyBar(pokemon2)
        background.paste(enmybar, (5, 23), enmybar)
        if x:
            newImage = Image.new(mode="RGBA", size=(x, y))
            newImage.paste(background, (0,0))
            background = newImage

        background.save("data/pokemon/compost.png", quality=100)
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
