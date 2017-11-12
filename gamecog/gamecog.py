from PIL import Image
import discord
from discord.ext import commands

class gamecog:
    """Weird experimental stuff"""
    def __init__(self, bot):
        self.bot = bot
        self.tileSize = 32
        self.width = 320
        self.height = 320
        self.image = Image.open("data/gamecog/level.png")
        self.pimage = Image.open("data/gamecog/player.png")
        self.pheight = 64
        self.pwidth = 64

        self.pbox = (64 * 3, 0, 64 * 4, 64)
        self.croppedp = self.pimage.crop(self.pbox)
        self.croppedp.save("data/gamecog/croppedplayer.png")

        self.box = (320, 320, 320 * 2, 320 * 2)
        self.cropped = self.image.crop(self.box)
        self.cropped.save("data/gamecog/croppedlevel.png")

        self.landcopy = self.cropped.copy()
        self.position = ((self.width / 2 - self.pwidth), (self.height / 2 - self.pheight))
        self.landcopy.paste(self.croppedp, self.position)
        self.landcopy.save("data/gamecog/composted.png")

    @commands.group(pass_context=True, name='game')
    async def _game(self, context):
        """Thunderdoge Game??"""
        if context.invoked_subcommand is None:
            prefix = context.prefix
            title = '**Thunderdoge Game**\n'
            description = '**Commands**\n\n'
            description += '``{0}game init``: Boots up one of them vidya games.\n'

            em = discord.Embed(title=title, description=description.format(prefix), color=discord.Color.blue())
            em.set_footer(text='This cog was made by Arrow.')
            await self.bot.say(embed=em)

    @_game.command(pass_context=True, name='init')
    async def _init(self, context):
        await self.bot.send_file(context.message.channel, 'data/gamecog/composted.png')