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
    
    named_colors = [
        "WHITE",
        "CYAN",
        "AQUA",
        "VIOLET",
        "PINK",
        "FUCHSIA",
        "YELLOW",
        "LGRAY",
        "SILVER",
        "RED",
        "LIME",
        "BLUE",
        "GRAY",
        "TEAL",
        "PURPLE",
        "OLIVE",
        "BLACK",
        "MAROON",
        "GREEN",
        "NAVY",
    ]
    
    # WHITE FF FF FF
    # CYAN 00 FF FF
    # AQUA 00 FF FF
    # VIOLET FF 00 FF
    # PINK FF 00 FF
    # FUCHSIA FF 00 FF
    # YELLOW FF FF 00
    # LGRAY C0 C0 C0
    # SILVER C0 C0 C0
    # RED FF 00 00
    # LIME 00 FF 00
    # BLUE 00 00 FF
    # GRAY 80 80 80
    # TEAL 00 80 80
    # PURPLE 80 00 80
    # OLIVE 80 80 00
    # BLACK 00 00 00
    # MAROON 80 00 00
    # GREEN 00 80 00
    # NAVY 00 00 80
    
    error_msg = [
        "Oops something went wrong",
        "Oopsie Doopsie, an error occured",
        "An error, occured has",
        "*scratches head* I think something went wrong",
        "Out of service, try again in 1 to 9325663 seconds"
    ]
    
    oob_paint_error = [
        "Tried to paint outside of the canvas, but the paint fell on the floor... Now who is gonne clean up the mess? (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Darnit, we havent invented paint that sticks to a non canvas area yet... (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Heard of a coloring book? Maybe practice drawing inside the lines in one of those. (Area is " + str(max_x) + "," + str(max_y) + ")",
        "COMPUTE ERROR, VALUE OUT-OF-BOUNDS (Area is " + str(max_x) + "," + str(max_y) + ")",
        "*sigh* Thats not ON the canvas... (Area is " + str(max_x) + "," + str(max_y) + ")",
        "I hope you aim better on the toilet than you are trying to paint ON the canvas... (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Sorry, I couldnt afford a bigger canvas, you have to paint on the one already here. (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Inside the lines.. INSIDE! (Area is " + str(max_x) + "," + str(max_y) + ")",
        "If you need help with the coordinate system, call 555-HELP-ME-I-CANT-COORDINATE (Area is " + str(max_x) + "," + str(max_y) + ")",
        "If you need help with the painting system, call 555-HELP-ME-I-CANT-PAINT (Area is " + str(max_x) + "," + str(max_y) + ")",
        "OK, I give up.. Pixel added outside of the bounds, for future reference the area is " + str(max_x) + "," + str(max_y) + "",
        "Pixel added! Wait.. Pixel added! Hmmm... Pixel added! I give up, cant place a pixel there as it seems it is outside of the canvas.. (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Pixel not added! (Area is " + str(max_x) + "," + str(max_y) + ")",
        ".... (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Do you need assistance? It does looks like it. (Area is " + str(max_x) + "," + str(max_y) + ")"        
    ]
    
    oob_clear_error = [
        "No point of clearing outside the canvas now, is there? (Area is " + str(max_x) + "," + str(max_y) + ")",
        "Hey bucko! Ever tried to use an eraser in the air? Its nott gonna work..(Area is " + str(max_x) + "," + str(max_y) + ")",
        "And you call yourself a moderator? And cant even keep it inside the bounds? (Area is " + str(max_x) + "," + str(max_y) + ")"
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

    @commands.group()
    @commands.guild_only()
    async def placeadmin(self, ctx):
        """BFEE Canvas painter admin commands"""
        pass
        
    @placeadmin.command(name="clear")
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
        if(int(y) > self.max_y):
            return await ctx.send(random.choice(self.oob_clear_error))
        if(int(x) < 1):
            return await ctx.send(random.choice(self.oob_clear_error))
        if(int(y) < 1):
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
            if (place_color.upper() not in self.named_colors):
                return await ctx.send("Not a valid color or HEX-Color ({0})".format(place_color))
            
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