import json
import random
import logging
from PIL import Image, ImageFont, ImageDraw

background = Image.open('data/sprites/background.png')
with open('data/pokemon.json') as rawPokemon:
    pokemonData = json.load(rawPokemon)
with open('data/moves.json') as rawMoves:
    moveData = json.load(rawMoves)
playerbar = Image.open('data/sprites/playerbar.png')
enemybar = Image.open('data/sprites/enemybar.png')
font = ImageFont.truetype('data/pokemonname.ttf', 10)
healthFont = ImageFont.truetype('data/pokemonname.ttf', 9)

level = random.randint(1, 100)
pokemon1 = pokemonData[random.randint(1, 150) - 1]
pokemon2 = pokemonData[random.randint(1, 150) - 1]
image1 = Image.open('data/sprites/' + str(pokemon1["id"]) + 'b.png').convert("RGBA")
image1 = image1.resize(size=(96 * 2, 96 * 2))
image2 = Image.open('data/sprites/' + str(pokemon2["id"]) + 'f.png').convert("RGBA")
background = background.copy()
background.paste(image2, (148, 15), image2)
background.paste(image1, (-20, int(200 - 96 * 1.75)), image1)
background.paste(enemybar, (5, 23), enemybar)
background.paste(playerbar, (142, 105), playerbar)
background = background.resize(size=(400, 255))
draw = ImageDraw.Draw(background)
#Enemy pokmeon name
draw.text((15, 37), str.capitalize(pokemon2["name"]), font=font, fill=(0, 0, 0, 255))
#Player pokemon name
draw.text((231, 184), str.capitalize(pokemon1["name"]), font=font, fill=(0, 0, 0, 255))
#Enemy pokmeon level
draw.text((146, 38), str(level), font=font, fill=(0, 0, 0, 255))
#Player pokemon level
draw.text((354, 185), str(level), font=font, fill=(0, 0, 0, 255))
#Player health
health = 100
leftPad = len(str(health))
draw.text((339 - (10) * leftPad, 211), str(health), font=healthFont, fill=(255, 255, 255, 255))
draw.text((350, 211), str(health), font=healthFont, fill=(255, 255, 255, 255))
background.save("data/compost.png", quality=100)




#self.bot.send_file(context.message.channel, 'data/pokemon/compost.png')


# pokemon = {}
# with open('data/pokemon.json') as rawPokemon:
#     pokemonData = json.load(rawPokemon)
#     pokemon = pokemonData[random.randint(1, 150) - 1]
    # with open('data/pokemon/moves.json') as rawMoves:
    #     movesData = json.load(rawMoves)
# pokemonMoveMax = len(pokemon["moves"]) - 1
#
# pokemon["learnedMoves"] = [
#     pokemon["moves"][random.randint(0, pokemonMoveMax)],
#     pokemon["moves"][random.randint(0, pokemonMoveMax)],
#     pokemon["moves"][random.randint(0, pokemonMoveMax)],
#     pokemon["moves"][random.randint(0, pokemonMoveMax)]
# ]
#
# pokemon["level"] = random.randint(1, 100)
#
# title = "Oh wow you caught a " + pokemon["name"] + "!"
# description = "PokeDex Number: " + str(pokemon["id"]) + "\n"
# description += "Height: " + str(pokemon["height"])
# description += " Weight: " + str(pokemon["weight"]) + "\n"
# description += "Level: " + str(pokemon["level"]) + "\n"
# description += "It knows " + pokemon["learnedMoves"][0]["name"] + ", "
# description += pokemon["learnedMoves"][1]["name"] + ", "
# description += pokemon["learnedMoves"][2]["name"] + ", "
# description += "and " + pokemon["learnedMoves"][3]["name"] + "!\n"
# description += "Base Stats:\n"
# description += "Speed: " + str(pokemon["stats"]["speed"]["base"]) + " HP: " + str(pokemon["stats"]["hp"]["base"]) + "\n"
# description += "Attack: " + str(pokemon["stats"]["attack"]["base"]) + " Special Attack: " + str(pokemon["stats"]["special-attack"]["base"]) + "\n"
# description += "Defense: " + str(pokemon["stats"]["defense"]["base"]) + " Special Defense: " + str(pokemon["stats"]["special-defense"]["base"]) + "\n"



logger = logging.getLogger("pokermans")
# logger.warning(title + description)