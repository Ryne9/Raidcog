from collections import deque
from enum import Enum
import random
from discord.ext import commands

class SMReel(Enum):
    cherries  = "CHERY"
    cookie    = "COKIE"
    flc       = "FLCCC"
    shibe     = "SHIBE"
    sunflower = "SUNFL"
    heart     = "HEART"

PAYOUTS = {
    (SMReel.shibe, SMReel.shibe, SMReel.shibe): {
        "payout" : lambda x: x * 35,
        "phrase" : "JACKPOT! ALL SHIBES! Your bid has been multiplied * 35!"
    },
    (SMReel.shibe, SMReel.shibe): {
        "payout" : lambda x: x * 5,
        "phrase" : "Two shibes! Your bid has been multiplied by 5!"
    },
    (SMReel.shibe): {
        "payout": lambda x: x * 2,
        "phrase": "One shibe! Your bid has been multiplied by 2!"
    },
    "3 symbols" : {
        "payout" : lambda x: x * 12,
        "phrase" : "Three symbols! Your bid has been multiplied by 12!"
    }
}

SLOT_PAYOUTS_MSG = ("Slot machine payouts:\n"
                    "{shibe.value} {shibe.value} {shibe.value} Bet * 35\n"
                    "{shibe.value} {shibe.value} Bet * 5\n"
                    "{shibe.value} Bet * 2\n"
                    "Three symbols: Bet * 12\n".format(**SMReel.__dict__))


default_settings = {"PAYDAY_TIME": 300, "PAYDAY_CREDITS": 120,
                    "SLOT_MIN": 5, "SLOT_MAX": 100, "SLOT_TIME": 0,
                    "REGISTER_CREDITS": 0}

class slotsim:
    """Thunderdoges D2 clan link!"""

    def __init__(self, bot):
        self.bot = bot

    def slot_machine_sim(self, bid, balance):
        default_reel = deque(SMReel)
        reels = []
        for i in range(3):
            default_reel.rotate(random.randint(-999, 999))  # weeeeee
            new_reel = deque(default_reel, maxlen=3)  # we need only 3 symbols
            reels.append(new_reel)  # for each reel
        rows = ((reels[0][0], reels[1][0], reels[2][0]),
                (reels[0][1], reels[1][1], reels[2][1]),
                (reels[0][2], reels[1][2], reels[2][2]))

        slot = "~~\n~~"  # Mobile friendly
        for i, row in enumerate(rows):  # Let's build the slot to show
            sign = "  "
            if i == 1:
                sign = ">"
            slot += "{}{} {} {}\n".format(sign, *[c.value for c in row])

        payout = PAYOUTS.get(rows[1])
        if not payout:
            # Checks for two-symbol special rewards
            payout = PAYOUTS.get((rows[1][0], rows[1][1]),
                                 PAYOUTS.get((rows[1][1], rows[1][2])),
                                 )
        if not payout:
            # Checks for other two-symbol rewards
            payout = PAYOUTS.get((rows[1][0], rows[1][2]))

        # Check one symbol rewards
        if not payout:
            payout = PAYOUTS.get(rows[1][0])
        if not payout:
            payout = PAYOUTS.get(rows[1][1])
        if not payout:
            payout = PAYOUTS.get(rows[1][2])

        if not payout:
            # Still nothing. Let's check for 3 generic same symbols
            has_three = rows[1][0] == rows[1][1] == rows[1][2]
            if has_three:
                payout = PAYOUTS["3 symbols"]

        if payout:
            then = balance
            pay = payout["payout"](bid)
            now = then - bid + pay
            return now
        else:
            then = balance
            now = then - bid
            return now

    @commands.command()
    async def slotsim(self, balance: int, biddiv: int, total: int):
        counter = 0
        totalTimesGoneBroke = 0
        wins = 0
        losses = 0

        while counter < total:
            bid = balance / biddiv
            prevBalance = balance
            balance = self.slot_machine_sim(bid, balance)
            if balance < 0:
                totalTimesGoneBroke += 1
            if balance > prevBalance:
                wins += 1
            else:
                losses += 1
            counter += 1

        await self.bot.say("Ending balance: " + balance + " and went broke: " + totalTimesGoneBroke + "times"
                           + "\nWins: " + wins + " Losses: " + losses)

def setup(bot):
    bot.add_cog(slotsim(bot))
