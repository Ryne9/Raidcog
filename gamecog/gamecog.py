from PIL import Image
import discord
import json
import random
from discord.ext import commands

image = Image.open("data/gamecog/level.png")
pimage = Image.open("data/gamecog/player.png")
sheet = Image.open("data/gamecog/tilesheet.png")
cropped = ""
croppedp = ""
random.seed()

chars = {
    "right": "➡",
    "left": "⬅",
    "up": "⬆",
    "down": "⬇"
}

charfacing = {
    "down": 1,
    "left": 2,
    "right": 3,
    "up": 4
}

class gamecog:
    """Weird experimental stuff"""
    def __init__(self, bot):
        self.bot = bot

        self.x = 320/64
        self.y = 320/64

        box = (self.x * 64, self.y * 64, self.x * 64 + 320, self.y * 64 + 320)
        self.cropped = image.crop(box)
        self.cropped = self.cropped.resize((160, 160), Image.ANTIALIAS)
        self.cropped.save("data/gamecog/croppedlevel.png", quality=60)

        box = (64 * 3, 0, 64 * 4, 64)
        self.croppedp = pimage.crop(box)
        self.croppedp = self.cropped.resize((32, 32), Image.ANTIALIAS)
        self.croppedp.save("data/gamecog/croppedplayer.png", quality=60)

        self.compost()

    def crop_player(self, face):
        box = (64 * 3, 64 * (charfacing[face] - 1), 64 * 4, 64 * charfacing[face])
        self.croppedp = pimage.crop(box)
        # self.croppedp = self.croppedp.resize((32, 32), Image.ANTIALIAS)
        self.croppedp.save("data/gamecog/croppedplayer.png", quality=30)

    def crop_land(self):
        box = (self.x * 64, self.y * 64, self.x * 64 + 320, self.y * 64 + 320)
        self.cropped = image.crop(box)
        # self.cropped = self.cropped.resize((160, 160), Image.ANTIALIAS)
        self.cropped.save("data/gamecog/croppedlevel.png", quality=30)

    def compost(self):
        landcopy = self.cropped.copy()
        position = (128, 128)
        landcopy.paste(self.croppedp, position, self.croppedp)
        landcopy.save("data/gamecog/composted.png", quality=30)

    @commands.group(pass_context=True, name='game')
    async def _game(self, context):
        """Thunderdoge Game??"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Thunderdoge Game**\n'
            description = '**Commands**\n\n'
            description += '``{0}game start``: Boots up one of them vidya games.\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_game.command(pass_context=True, name="generate")
    async def _generate(self, context, size:int):
        with open('data/gamecog/tileset.json') as data_file:
            data = json.load(data_file)
            output = Image.new(mode="RGB", size=(size * 32, size * 32))
            pos = []
            for item in data:
                print(item)
                pos.append(data[item])
            for x in range(0, size - 1):
                for y in range(0, size -1):
                    randTile = random.randint(0, 11)
                    print(pos[randTile])
                    box = (pos[randTile]["x"] * 32, pos[randTile]["y"] * 32, 32 + pos[randTile]["x"] * 32, 32 + pos[randTile]["y"] * 32)
                    image = sheet.crop(box)
                    pastePosition = (x * 32, y * 32)
                    output.paste(image, pastePosition)
            output.save("data/gamecog/output.png", quality=30)
        await self.bot.send_file(context.message.channel, 'data/gamecog/output.png')

    @_game.command(pass_context=True, name="generate_yolo")
    async def _generate_yolo(self, context, size:int):
        output = Image.new(mode="RGB", size=(size * 32, size * 32))
        for x in range(0, size):
            for y in range(0, size):
                tx = random.randint(0, 40)
                ty = random.randint(2, 13)
                box = (tx * 32, tx * 32, 32 + tx * 32, 32 + ty * 32)
                image = sheet.crop(box)
                pastePosition = (x * 32, y * 32)
                output.paste(image, pastePosition)
        output.save("data/gamecog/output.png", quality=30)
        await self.bot.send_file(context.message.channel, 'data/gamecog/output.png')

    @_game.command(pass_context=True, name="start")
    async def _start(self, context, timeout: int=30):
        return await self.game(context, timeout)

    async def game(self, context, timeout: int=30):
        expected = ["➡", "⬅", "⬆", "⬇"]
        message = \
            await self.bot.send_file(context.message.channel, 'data/gamecog/composted.png')
        await self.bot.add_reaction(message, chars["left"])
        await self.bot.add_reaction(message, chars["up"])
        await self.bot.add_reaction(message, chars["down"])
        await self.bot.add_reaction(message, chars["right"])
        react = await self.bot.wait_for_reaction(
            message=message, user=context.message.author, timeout=timeout,
            emoji=expected
        )
        if react is None:
            try:
                try:
                    await self.bot.delete_message(message)
                    await self.bot.clear_reactions(message)
                except:
                    await self.bot.remove_reaction(message, chars["left"], self.bot.user)
                    await self.bot.remove_reaction(message, chars["up"], self.bot.user)
                    await self.bot.remove_reaction(message, chars["down"], self.bot.user)
                    await self.bot.remove_reaction(message, chars["right"], self.bot.user)
            except:
                pass
            return None
        reacts = {v: k for k, v in chars.items()}
        react = reacts[react.reaction.emoji]
        if react == "left":
            self.crop_player("left")
            if self.x > 0:
                self.x -= 1
                self.crop_land()
            self.compost()
            try:
                await self.bot.delete_message(message)
            except:
                pass
            return await self.game(context, timeout=timeout)
        elif react == "right":
            self.crop_player("right")
            if self.x < 16:
                self.x += 1
                self.crop_land()
            self.compost()
            try:
                await self.bot.delete_message(message)
            except:
                pass
            return await self.game(context, timeout=timeout)
        elif react == "up":
            self.crop_player("up")
            if self.y > 0:
                self.y -= 1
                self.crop_land()
            self.compost()
            try:
                await self.bot.delete_message(message)
            except:
                pass
            return await self.game(context, timeout=timeout)
        elif react == "down":
            self.crop_player("down")
            if self.y < 16:
                self.y += 1
                self.crop_land()
            self.compost()
            try:
                await self.bot.delete_message(message)
            except:
                pass
            return await self.game(context, timeout=timeout)


def setup(bot):
    bot.add_cog(gamecog(bot))