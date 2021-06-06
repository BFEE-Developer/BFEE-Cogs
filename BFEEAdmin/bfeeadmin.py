import discord
import aiohttp
from bs4 import BeautifulSoup
from typing import Optional
from random import randint
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path
from .rankcard import RankCard
from .db import DBUtils
from .utils import Utils
from redbot.core.utils import AsyncIter
class BFEEAdmin(commands.Cog):
    
    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    # Variables
    default_guild = {
        "blockroles": [],
    }
    
    
    @commands.group()
    @checks.admin()
    @commands.guild_only()
    async def locksettings(self, ctx):
        """Locksettings configuration commands."""
        pass
        
    @locksettings.group()
    @checks.admin()
    @commands.guild_only()
    async def addrole(self, ctx, role: discord.Role = None):
        """Add role to lockdown."""
        if role is None:
            return
        if role.id not in await self.blockroles(ctx.guild):
            await self._add_block_role(ctx.guild, role.id)
            await ctx.send("Role added")
        else:
            await ctx.send("Role already blacklisted")
            
    @locksettings.group()
    @checks.admin()
    @commands.guild_only()
    async def delrole(self, ctx, role: discord.Role = None):
        """Remove role from lockdown."""
        if role is None:
            return
        if role.id not in await self.blockroles(ctx.guild):
            await ctx.send("Role not in list")
        else:
            await self._del_block_role(ctx.guild, role.id)
            await ctx.send("Role removed")
    
    locksettings.group()
    @checks.admin()
    @commands.guild_only()
    async def listroles(self, ctx):
        """Lists roles in lockdown."""
        emb = discord.Embed()
        emb.title = "List of roles who will be lockdowned."
        emb.description = "These roles will be affected by the lockdown command."
        roles = await self.blockroles(ctx.guild)
        if not len(roles):
            return await ctx.send("No roles configured")
        emb.add_field(
            name="Roles:", value="\n".join([ctx.guild.get_role(x).mention for x in roles])
        )
        await ctx.send(embed=emb)
            
    async def _add_block_role(self, guild, role):
        async with self.config.guild(guild).blockroles() as rolelist:
            rolelist.append(role)
            
    async def _del_block_role(self, guild, role):
        async with self.config.guild(guild).blockroles() as rolelist:
            rolelist.remove(role)  
    
    # permissions = discord.Permissions()
    # permissions.update(kick_members = False)
    # await role.edit(reason = None, colour = discord.Colour.blue(), permissions=permissions, add_reactions=False)