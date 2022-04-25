import discord
import requests
import re
import random
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path
from redbot.core.utils import menus
from redbot.core.utils.chat_formatting import box, pagify, escape, humanize_list

class BFEEPlace(commands.Cog):
    """BFEE Place Cog"""

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    default_guild = {}
    max_x = 640
    max_y = 480

    post_url = "https://place.bfee.co/addCord.php"
    
    error_msg = [
        "Oops something went wrong",
        "Oopsie Doopsie, an error occured",
        "An error, occured has",
        "*scratches head* I think something went wrong",
        "Out of service, try again in 1 to 9325663 seconds"
    ]
    
    oob_paint_error = [
        "Tried to paint outide of the canvas, but the paint fell on the floor... Now who is gonne clean up the mess? (" + max_x + "," + max_y + ")",
        "Darnit, we havent invented paint that sticks to a non canvas area yet... (" + max_x + "," + max_y + ")",
        "Heard of a coloring book? Maybe practice drawing inside the lines in one of those. (" + max_x + "," + max_y + ")",
        "COMPUTE ERROR, VALUE OUT-OF-BOUNDS (" + max_x + "," + max_y + ")",
        "*sigh* Thats not ON the canvas... (" + max_x + "," + max_y + ")",
        "I hope you aim better on the toilet than you are trying to paint ON the canvas... (" + max_x + "," + max_y + ")"
    ]
    
    oob_clear_error = [
        "No point of clearing outside the canvas now, is there? (" + max_x + "," + max_y + ")",
        "Hey bucko! Ever tried to use an eraser in the air? Its nott gonna work.. (" + max_x + "," + max_y + ")",
        "And you call yourself a moderator? And cant even keep it inside the bounds? (" + max_x + "," + max_y + ")"
    ]

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
            statsuser = discord.utils.get(client.users, name=data["user"], discriminator=data["disc"])
            #await ctx.send("{0} has placed {1} pixels in {2} days.".format(statsuser.mention, data["pixels"], data["days"]))
            await ctx.send("{0} has placed {1} pixels in {2} days.".format(data["user"], data["pixels"], data["days"]))
        except requests.exceptions.Timeout:
            await ctx.send(random.choice(self.error_msg))
        except requests.exceptions.TooManyRedirects:
            await ctx.send(random.choice(self.error_msg))
        except discord.Forbidden:
            await ctx.send(random.choice(self.error_msg))
            
    @place.command(name="clear")
    @checks.admin()
    @commands.guild_only()
    async def _clear(self, ctx, x: str = None, y: str = None, w: str = None, h: str = None):
        """Clears an area of the canvas"""
        
        if not x:
            return await ctx.send_help()
        if not y:
            return await ctx.send_help()
        if not w:
            return await ctx.send_help()
        if not h:
            return await ctx.send_help()
            
        if(int(x) > self.max_x):
            return await ctx.send(random.choice(self.oob_clear_error))
        if(int(place_y) > self.max_y):
            return await ctx.send(random.choice(self.oob_clear_error))
        if(int(place_x) < 1):
            return await ctx.send(random.choice(self.oob_clear_error))
        if(int(place_y) < 1):
            return await ctx.send(random.choice(self.oob_clear_error))
            
        clear_user = ctx.message.author.name
        try:
            post_obj = {'type': 'clear', 'x': x, 'y': y, 'w': w, 'h': h, 'user': clear_user}
            x = requests.post(self.post_url, data = post_obj)
        except requests.exceptions.Timeout:
            await ctx.send(random.choice(self.error_msg))
        except requests.exceptions.TooManyRedirects:
            await ctx.send(random.choice(self.error_msg))
        except discord.Forbidden:
            await ctx.send(random.choice(self.error_msg))
        
        await ctx.send("Cleared!")
        

    @place.command(name="put")
    @commands.guild_only()
    async def _put(self, ctx, x: str = None, y: str = None, color: str = None):
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
            return await ctx.send(random.choice(self.oob_paint_error))
        if(int(place_y) > self.max_y):
            return await ctx.send(random.choice(self.oob_paint_error))
        if(int(place_x) < 1):
            return await ctx.send(random.choice(self.oob_paint_error))
        if(int(place_y) < 1):
            return await ctx.send(random.choice(self.oob_paint_error))

        try:
            post_obj = {'type': 'put', 'x': place_x, 'y': place_y, 'color': place_color, 'user': place_user}
            x = requests.post(self.post_url, data = post_obj)
        except requests.exceptions.Timeout:
            await ctx.send(random.choice(self.error_msg))
        except requests.exceptions.TooManyRedirects:
            await ctx.send(random.choice(self.error_msg))
        except discord.Forbidden:
            await ctx.send(random.choice(self.error_msg))

        if x.text == "OK":
            await ctx.send("Pixel added")
        else:
            await ctx.send(random.choice(self.error_msg))