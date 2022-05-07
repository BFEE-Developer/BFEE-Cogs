import discord
import re
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path
from datetime import datetime, timezone, timedelta
from .utils import BFEEdb

class BFEEGiveaway(commands.Cog):
    """BFEE Giveaway"""

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    UNITS = {
        "seconds": ["s", "sec", "second"],
        "month":  ["month"], 
        "minutes": ["m", "min", "minute"], 
        "hours":   ["h", "hour"],
        "days":    ["d", "day"], 
        "weeks":   ["w", "week"], 
        "year":   ["year"]
    }
    DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    digits = "|".join(f"{i}" for i in DIGITS)
    units = "|".join(r"(?P<{}>{})".format(i, "|".join(value)) for i, value in UNITS.items())
    TIME_UNITS = re.compile(r"(?i)(?P<value>[\d\.,]+) ?(?P<unit>{})".format(units))
    
    def __init__(self, bot):
        self.bot = bot        
        self.config = Config.get_conf(self, identifier=13378347487433784274, force_registration=True)
        self.config.register_guild(**self.default_guild)

    @commands.group()
    @checks.mod()
    @commands.guild_only()
    async def ga(self,ctx):
        """Giveaways"""
        pass

    @bfeegiveaway.command(name="create")
    @checks.mod()
    @commands.guild_only()
    async def _create(self, ctx, prize: str, duration: str, channel: discord.Channel, user: discord.User, description: str = None, winners: int = 1, reaction: str = '🎉'):
        """Create a new giveaway
        Parameters:
        prize:
            The prize
        duration:
            The duration of the giveaway, digit followed by either s, m, h, d, or w.
            s = seconds
            m = minutes
            h = hours
            d = days
            w = weeks
            eg. 2w 1d 4h 37m 28s
        description:
            [OPTIONAL]
            The description of the giveaway
        winners:
            [OPTIONAL]
            Amount of winners.
            Default: 1
        reaction:
            [OPTIONAL]
            Which emote to use for the giveaway, can also use multiple (seperated by ,)
            Default: 🎉
        channel:
            Which channel the giveaway should be hosted in
        user:
            [OPTIONAL]
            Which user that is making the giveaway
        """
        
        if not prize:
            return await ctx.send_help()
        if not duration:
            return await ctx.send_help()
        if not channel:
            return await ctx.send_help()
            
        ga_deadline = datetime.now(tz=timezone.utc) + getSeconds(duration)
        ga_msg = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
        embed.setFooter(text="WHEN_GIVEAWAY_ENDS")
        embed.setTimestamp(finish.isoformat())
        embed.setTitle("TITLE")
        embed.setDescription("DESCRIPTION")
        await ctx.send(embed=embed)
        
        # React to MESSAGE
        # Store MSGID somewhere
        # Store giveaway somewhere
        
        await ctx.reply("Created", private=True)
    
    @bfeegiveaway.command(name="delete")
    @checks.admin()
    @commands.guild_only()
    async def _delete(self, ctx, msg_id: int): #Snowflake?
        pass
        
    def getSeconds(duration: str) -> timedelta:
        total = timedelta()
        for d in self.TIME_UNITS.finditer(duration):
            interval, unit = d.group("value"), [i for i in filter(lambda x: x[1], d.groupdict().items())][-1][0]
            interval = interval.replace(',','.')
            if interval == '.':
                continue
            if interval.isalpha():
                interval = self.DIGITS.index(interval.lower())
            interval = float(interval)
            if unit == 'month':
                interval *= 30
                unit = "days"
            elif unit == "year":
                interval *=365
                unit = "days"
            total += timedelta(**{unit: interval})
        return total