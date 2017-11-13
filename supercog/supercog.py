import discord
import json
import random

from cogs.utils.dataIO import dataIO
from discord.ext import commands

class supercog:
    """Weird experimental stuff"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, name='super')
    async def _super(self, context):
        """Superhero card game!"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Superhero Card Game**\n'
            description = '**Commands**\n\n'
            description += '``{0}super deal``: Deals a set of black/white superhero cards!\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    def generate_card(self, type):
        if type == "w":
            with open('data/supercog/whitecards.json') as wcards:
                w = json.load(wcards)
                return w[random.randint(0, len(w) - 1)]
        else:
            with open('data/supercog/blackcards.json') as bcards:
                b = json.load(bcards)
                return b[random.randint(0, len(b) - 1)]

    @_super.command(pass_context=True, name="generate")
    async def _generate(self, context):
        with open('data/supercog/blackcards.json') as bcards:
            b = json.load(bcards)
        with open('data/supercog/whitecards.json') as wcards:
            w = json.load(wcards)
        await self.bot.say("Your Superfight cards:\nWhite Card: " + w[random.randint(0, len(w) - 1)] + " Black Card: " +
                           b[random.randint(0, len(b) - 1)])

    @_super.command(pass_context=True, name="newgame")
    async def _newgame(self, context):
        newGame = [{
            "player": context.message.author.id,
            "whiteCard": "",
            "blackCard": ""
        }]
        with open('data/supercog/players.json', "w") as tonuke:
            json.dump(newGame, tonuke)
        await self.bot.say("You have started a new Superhero game! Have others join the game "
                           "with {0}super join\n".format(context.prefix))

    @_super.command(pass_context=True, name="join")
    async def _join(self, context):
        with open('data/supercog/players.json', "r") as players_file:
            players = json.load(players_file)
            for player in players:
                if player["player"] == context.message.author.id:
                    await self.bot.say("You're already in this game!")
                    return
            newPlayer = {
                "player": context.message.author.id,
                "whiteCard": "",
                "blackCard": ""
            }
            players.append(newPlayer)
        with open('data/supercog/players.json', 'w') as players_file:
            json.dump(players, players_file)
        await self.bot.say("You have joined the game!")

    @_super.command(pass_context=True, name="deal")
    async def _deal(self, context):
        with open('data/supercog/players.json', "r") as players_file:
            players = json.load(players_file)
            for player in players:
                dealtWhite = [
                    self.generate_card("w"),
                    self.generate_card("w"),
                    self.generate_card("w")
                ]
                dealtBlack = [
                    self.generate_card("b"),
                    self.generate_card("b"),
                    self.generate_card("b")
                ]
                player['dealtWhite'] = dealtWhite
                player['dealtBlack'] = dealtBlack
                user = discord.User(id=str(player["player"]))
                wlist = ""
                blist = ""
                for card in dealtWhite:
                    wlist += card + "\n"
                for card in dealtBlack:
                    blist += card + "\n"
                await self.bot.send_message(user, "Your white cards:\n" + wlist + "\n"
                                            "Your black cards:\n" + blist)
        with open("data/supercog/players.json", "w") as players_file:
            json.dump(players, players_file)
        await self.bot.say("All cards sent out.")

def check_files():
    f = "data/supercog/players.json"
    if not dataIO.is_valid_json(f):
        print("Creating default game's players.json...")
        dataIO.save_json(f, [])
    f = "data/supercog/game.json"
    if not dataIO.is_valid_json(f):
        print("Creating default game's game.json...")
        dataIO.save_json(f, [])

def setup(bot):
    check_files()
    bot.add_cog(supercog(bot))
