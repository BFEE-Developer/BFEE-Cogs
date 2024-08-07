import discord
import re
import random
import math
import base64
import copy
from .gamefw import GameFramework
from .eventcard import EventCard
from typing import Optional, Union
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path

class BFEEGames(commands.Cog):
    
    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.3"
    
    default_guild = {
        "players": [],
        "gameleaderrole": ""
    }
    
    player_obj = {
        "name": "",
        "id": "",
        "district": 0,
        "alive": True,
        "kills": 0,
        "deathcause": "",
        "avatar": ""
    }
    
    gf = GameFramework()
    eventcard = EventCard()
    
    def __init__(self, bot):
        self.bot = bot        
        self.config = Config.get_conf(
            self, identifier=133234277487767764274,
            force_registration=True
        )
        self.config.register_guild(**self.default_guild)
        self.eventcard.setBot(bot)
    
    @commands.group()
    @commands.guild_only()
    async def bfeegames(self, ctx):
        """BFEE games configuration commands."""
        pass
    
    @bfeegames.command(name="load")
    @checks.admin()
    @commands.guild_only()
    async def _load(self, ctx):
        """
        Sets a custom events file to be used
        You need to attach a file to this command, and it's extension needs to be `.json`.
        """
        await ctx.trigger_typing()
        if not ctx.message.attachments:
            return await ctx.send_help()
        file = ctx.message.attachments[0]
        if not file.filename.lower().endswith(".json"):
            await ctx.message.delete()
            return await ctx.send("Must be a json file.")
            
        await ctx.message.attachments[0].save(str(cog_data_path(self) / "events.json"))
        await ctx.message.delete()
        await ctx.send("Loaded custom events")
        
    @bfeegames.command(name="gameleader")
    @checks.admin()
    @commands.guild_only()
    async def _gameleader(self, ctx, role: discord.Role = None):
        """
        Tell the game which role is the gameleader role
        """
        print("sdgjhsjgh")
        if role is None:
            print("isnone")
            gleader = await self.config.guild(ctx.guild).gameleaderrole()
            if gleader is "":
                await ctx.send("There are no role configured")
            else:
                await ctx.send("Gameleader role is:\n ``{0}``".format(ctx.guild.get_role(gleader).name))
            return
        await self.config.guild(ctx.guild).gameleaderrole.set(role.id)
        await ctx.send("Added {0}".format(role.name))
    
    @bfeegames.command(name="start")
    @commands.guild_only()
    async def _start(self, ctx):
        """
        Start a new BFEE Hunger Games
        """
        if not await self._check_if_gameleader(ctx.guild, ctx.author):
            return
        owner = ctx.author
        ret = self.gf.new_game(ctx.channel.id, owner.id, owner.name)
        
        if ret.get('status') is not None:
            if ret["status"] is "GAMESTARTED":
                await ctx.send("Game already started by ``{0}``".format(ctx.guild.get_member(ret["owner"]).name))
                return
        
        #await ctx.send("{0} has started BFEE Hunger Games!\nPreparing game...".format(owner.mention))
                   
        ps = await self.config.guild(ctx.guild).get_raw("players")
        random.shuffle(ps)
        for x in ps:
            ret = await self.gf.add_player(ctx.channel.id, str(cog_data_path(self) / "{0}.png".format(x)), ctx.guild.get_member(x))
        
        ret = self.gf.start_game(ctx.channel.id, ctx.author.id)
        
        if ret.get('status') is not None:
            if ret.get('status') is "NOTENOUGHPLAYERS":
                await ctx.send("Not enough players to start BFEE Hunger Games!")
                return
            if ret.get('status') is "GAMEALREADYSTARTED":
                await ctx.send("Game is already started!")
                return
            if ret.get('status') is "NOTOWNER":
                await ctx.send("You are not the owner of this game!")
                return
            
       
        embed = discord.Embed(title=ret['title'], description=ret['description'])
        embed.set_footer(text=ret['footer'])
        self.lastday = 0
        await ctx.send(embed=embed)
        
    @bfeegames.command(name="listplayers")
    @commands.guild_only()
    async def _listplayers(self, ctx, user: discord.User = None):
        """
        Lists all players participating in BFEE Hunger Games
        """
        if not self._check_if_gameleader(ctx.guild, ctx.author):
            return
        msg = []
        ps = await self.config.guild(ctx.guild).get_raw("players")
        if len(ps) == 0:
            await ctx.send("There are no players")
            return
        for x in ps:
            print(x)
            if ctx.guild.get_member(int(x)) == None:
                async with self.config.guild(ctx.guild).players() as pl:
                    pl.remove(x)
            else:
                msg.append("★ {0}".format(ctx.guild.get_member(int(x)).name))
                #msg.append("★ {0} ({1})".format(ctx.guild.get_member(int(x)).name, int(x)))
        embed = discord.Embed(title="These are our brave souls", description="\n".join(msg))
        embed.set_footer(text="BFEE Hunger Games participants")
        await ctx.send(embed=embed)
                
    @bfeegames.command(name="add")
    @commands.guild_only()
    async def _add(self, ctx, user: discord.User = None):
        """
        Add a user to the game
        """
        if not await self._check_if_gameleader(ctx.guild, ctx.author):
            return
        if user is None:
            return await ctx.send_help()
        async with self.config.guild(ctx.guild).players() as pl:
            if user.id in pl:
                await ctx.send("``{0}`` is already registered".format(user.name))
                return
            pl.append(user.id)
            await self.dl_avatar(ctx, user.id)

        await ctx.send("Added ``{0}`` to BFEE Hunger Games".format(user.name))
        
    @bfeegames.command(name="updateavatar")
    @commands.guild_only()
    async def _updateavatar(self, ctx, user: discord.User = None):
        """
        Updates the avatar of a user
        """
        if not self._check_if_gameleader(ctx.guild, ctx.author):
            return
        if user is None:
            return await ctx.send_help()
        async with self.config.guild(ctx.guild).players() as pl:
            if user.id in pl:
                await self.dl_avatar(ctx, user.id)
            else:
                await ctx.send("``{0}`` is not part of the BFEE Hunger Games".format(user.name))
                return

        await ctx.send("Updated ``{0}'s`` avatar".format(user.name))
    
    @bfeegames.command(name="wipe")
    @checks.admin()
    @commands.guild_only()
    async def _wipe(self,ctx):
        """
        Removes everyone from the games
        """
        async with self.config.guild(ctx.guild).players() as pl:
            for x in pl:
                pl.remove(x)
                await ctx.send("Removed ``{0}`` from BFEE Hunger Games".format(ctx.guild.get_member(x).name))
    
    @bfeegames.command(name="remove")
    @commands.guild_only()
    async def _remove(self, ctx, user: discord.User = None):
        """
        Remove a user from the game
        """
        if not self._check_if_gameleader(ctx.guild, ctx.author):
            return
        if user is None:
            return await ctx.send_help()
        async with self.config.guild(ctx.guild).players() as pl:
            if user.id not in pl:
                await ctx.send("``{0}`` is not registered".format(user.name))
                return
            pl.remove(user.id)

        await ctx.send("Removed ``{0}`` from BFEE Hunger Games".format(user.name))
        
    @bfeegames.command(name="end")
    @commands.guild_only()
    async def end(self, ctx):
        """
        Cancels the current game in the channel.
        """
        if not self._check_if_gameleader(ctx.guild, ctx.author):
            return
        ret = self.gf.end_game(ctx.channel.id, ctx.author.id)
        await ctx.send("BFEE Hunger Games has been cancelled.")


    @commands.command(name="step")
    @commands.guild_only()
    async def step(self, ctx):
        """
        Steps forward the current game in the channel by one round.
        """
        if not self._check_if_gameleader(ctx.guild, ctx.author):
            return
        ret = self.gf.step(ctx.channel.id, ctx.author.id)
        
        if ret.get('status') is not None:
            if ret["status"] is "NOGAME":
                await ctx.send("No game is running")
                return
            if ret["status"] is "NOTOWNER":
                await ctx.send("Game already started by ``{0}``".format(ctx.guild.get_member(ret["owner"]).name))
                return
       
        if ret.get('day') is not None:
            if self.lastday is not ret["day"]:
                self.lastday = ret["day"]
                if ret["day"] is 1:
                    embed = discord.Embed(title="Bloodbath", color=ret['color'], description="Day {0}".format(ret["day"]))
                else:
                    embed = discord.Embed(title="Day {0}".format(ret["day"]), color=ret['color'], description="The sun rises")
                await ctx.send(embed=embed)
       
        try:
            avatars = ret["avatars"]
            if avatars is None:
                embed = discord.Embed(title=ret['title'], color=ret['color'], description=ret['description'])
                if ret['footer'] is not None:
                    embed.set_footer(text=ret['footer'])
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Night {0}".format(ret["day"]), color=ret['color'], description="The sun settles")
                await ctx.send(embed=embed)
            else:
                filen = await self.eventcard.get_card(ctx, ret["description"], avatars)
                await ctx.send(file=filen)
        except KeyError:
            avatars = None
            embed = discord.Embed(title=ret['title'], color=ret['color'], description=ret['description'])
            if ret['footer'] is not None:
                embed.set_footer(text=ret['footer'])
            await ctx.send(embed=embed)
        
    async def dl_avatar(self, ctx, id):
        if not (cog_data_path(self) / "{0}.png".format(id)).is_file():
            await ctx.guild.get_member(id).avatar_url.save(cog_data_path(self) / "{0}.png".format(id))
        return True
        
    async def _check_if_gameleader(self, guild, user: discord.User = None):
        if user.guild_permissions.kick_members:
            print("True")
            return True
        gleader = await self.config.guild(guild).gameleaderrole() 
        gleader_role = discord.utils.get(guild.roles, id=gleader)
        print(gleader_role)
        if gleader_role in user.roles:
            print("True")
            return True
        print("False")
        return False 