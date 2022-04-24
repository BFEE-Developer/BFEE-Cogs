import discord
import requests
import re
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path
from redbot.core.utils import menus
from redbot.core.utils.chat_formatting import box, pagify, escape, humanize_list

class BFEEPlace(commands.Cog):
    """BFEE Place Cog"""

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    default_guild = {}
    max_x = 600
    max_y = 600

    post_url = "https://place.bfee.co/addCord.php"

    def __init__(self, bot):
        self.bot = bot        
        self.config = Config.get_conf(self, identifier=13378942487733784001, force_registration=True)
        self.config.register_guild(**self.default_guild)

    def cog_unload(self):
        pass
        
    @commands.group()
    @commands.guild_only()
    async def place(self, ctx):
        """BFEE Canvas painter"""
        pass
        
    @place.command(name="stats")
    @commands.guild_only()
    async def _stats(self, ctx, user: discord.User = None):
        """Prints statistics about the user"""
        client = discord.Client()
        try:
            post_obj = {'type': 'stats', 'user': user}
            x = requests.post(self.post_url, data = post_obj)
            data = x.json()
            user = discord.utils.get(client.users, name=data["user"], discriminator=data["disc"])
            await ctx.send("{0} has placed {1} pixels in {2} days.".format(user.mention, data["pixels"], data["days"]))
        except discord.Forbidden:
            pass

    @place.command(name="put")
    @commands.guild_only()
    async def _put(self, ctx, *, x: str = None, y: str = None, color: str = None):
        """Places a pixel on the canvas
        
        Usage: !place put X, Y, COLOR
        Usage for Mazt3rz: !place put X, Y, COLOUR
        
        URL: https://place.bfee.co
        """
        if not x:
            return await ctx.send_help()
        if not y:
            return await ctx.send_help()
        if not color:
            return await ctx.send_help()

        place_x = x
        place_y = y
        place_color = color
        place_user = ctx.message.author.name
        
        if not place_x.isdigit():
            return await ctx.send("Not a valid X coordinate ({0})".format(place_x))
        if not place_y.isdigit():
            return await ctx.send("Not a valid Y coordinate ({0})".format(place_y))
            
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', place_color)
        if not match:
            return await ctx.send("Not a HEX-Color ({0})".format(place_color))
            
        if(int(place_x) > self.max_x):
            return await ctx.send("X coordinate is outside of the bounds ({}))".format(self.max_x))
        if(int(place_y) > self.max_y):
            return await ctx.send("Y coordinate is outside of the bounds ({}))".format(self.max_y))
        if(int(place_x) < 1):
            return await ctx.send("Tried to paint outide of the canvas, but the paint fell on the floor...")
        if(int(place_y) < 1):
            return await ctx.send("Tried to paint outide of the canvas, but the paint fell on the floor...")

        try:
            post_obj = {'type': 'put', 'x': place_x, 'y': place_y, 'color': place_color, 'user': place_user}
            x = requests.post(self.post_url, data = post_obj)
        except discord.Forbidden:
            pass

        if x.text == "OK":
            return await ctx.send("Pixel added")
        else:
            await ctx.send("Something went wrong, try again.")