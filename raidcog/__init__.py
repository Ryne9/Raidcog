from .raidcog import raidcog

# def check_files():
#     f = "data/raidcog/raids.json"
#     if not dataIO.is_valid_json(f):
#         print("Creating default raids's settings.json...")
#         dataIO.save_json(f, [])
def setup(bot):
    bot.add_cog(raidcog())