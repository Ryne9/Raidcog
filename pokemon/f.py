import json
import random
import logging
from PIL import Image

background = Image.open('data/sprites/battlebackground.png')

with open('data/pokemon.json') as rawPokemon:
    pokemonData = json.load(rawPokemon)
    pokemon1 = pokemonData[random.randint(1, 150) - 1]
    pokemon2 = pokemonData[random.randint(1, 150) - 1]
image1 = Image.open('data/sprites/' + str(pokemon1["id"]) + 'b.png').convert("RGBA")
image1 = image1.resize(size=(96 * 2, 96 * 2))
image2 = Image.open('data/sprites/' + str(pokemon2["id"]) + 'f.png').convert("RGBA")
background = background.copy()
background.paste(background)
background.paste(image2, (165, 5), image2)
background.paste(image1, (10, int(200 - 96 * 1.75)), image1)
background.save("data/compost.png", quality=30)
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