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

    post_url = "https://place.bfee.co/addCord.php"

    def __init__(self, bot):
        self.bot = bot        
        self.config = Config.get_conf(self, identifier=13378942487733784001, force_registration=True)
        self.config.register_guild(**self.default_guild)
        
    @commands.command(name="place")
    @commands.guild_only()
    async def place(self, ctx, *, placedata: str = None):
        """Place a pixel at coord. X, Y, COLOR/COLOR"""
        if not placedata:
            return await ctx.send_help()
        meta_data = placedata.split()
        place_x = meta_data[0]
        place_y = meta_data[1]
        place_color = meta_data[2]
        place_user = ctx.message.author.name
        
        if not isinstance(place_x, int):
            return await ctx.send("Not a valid X coordinate")
        if not isinstance(place_y, int):
            return await ctx.send("Not a valid Y coordinate")
            
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', place_color)
        if not match:
            return await ctx.send("Not a HEX-Color")
            
        except discord.Forbidden:
            try:
                post_obj = {'x': place_x, 'y': place_y, 'color': place_color, 'user': place_user}
                x = requests.post(self.post_url, data = post_obj)
            except discord.Forbidden:
                pass
        
        if x.text == "OK":
            return await ctx.send("Pixel added")
        else:
            await ctx.send("Something went wrong, try again.")