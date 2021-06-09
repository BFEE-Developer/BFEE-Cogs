import discord
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path

class BFEEAdmin(commands.Cog):
    
    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    # Variables
    default_guild = {
        "blockroles": [],
    }
    
    def __init__(self, bot):
        self.bot = bot        
        self.config = Config.get_conf(self, identifier=13378427487733784274, force_registration=True)
        self.config.register_guild(**self.default_guild)
        
    @commands.command(name="lockserver")
    @checks.admin()
    @commands.guild_only()
    async def _lockserver(self,ctx):
        """Lockdown the server"""
        await self._lockdown(ctx)
        try:
            await ctx.send("Server is now in LOCKDOWN!")
        except:
            pass
        
    @commands.command(name="unlockserver")
    @checks.admin()
    @commands.guild_only()
    async def _unlockserver(self,ctx):
        """End the lockdown"""
        await self._unlock(ctx)
        try:
            await ctx.send("Lockdown has ended.")
        except:
            pass
    
    @commands.group()
    @checks.admin()
    @commands.guild_only()
    async def locksettings(self, ctx):
        """Locksettings configuration commands."""
        pass
        
    @locksettings.command(name="addrole")
    @checks.admin()
    @commands.guild_only()
    async def _addrole(self, ctx, role: discord.Role = None):
        """Add role to lockdown."""
        if role is None:
            return
        if role.id not in await self._get_block_roles(ctx.guild):
            await self._add_block_role(ctx.guild, role.id)
            try:
                await ctx.send("Role added")
            except:
                pass
        else:
            try:
                await ctx.send("Role already in list")
            except:
                pass
            
    @locksettings.command(name="delrole")
    @checks.admin()
    @commands.guild_only()
    async def _delrole(self, ctx, role: discord.Role = None):
        """Remove role from lockdown."""
        if role is None:
            return
        if role.id not in await self._get_block_roles(ctx.guild):
            try:
                await ctx.send("Role not in list")
            except:
                pass
        else:
            await self._del_block_role(ctx.guild, role.id)
            try:
                await ctx.send("Role removed")
            except:
                pass
    
    @locksettings.command(name="listroles")
    @checks.admin()
    @commands.guild_only()
    async def _listroles(self, ctx):
        """Lists roles in lockdown."""
        try:
            ctx.send("List of roles who will be lockdowned:\n\n".join([ctx.guild.get_role(x).name for x in roles]))
        except:
            pass
        #emb = discord.Embed()
        #emb.title = "List of roles who will be lockdowned."
        #emb.description = "These roles will be affected by the lockdown command."
        #roles = await self._get_block_roles(ctx.guild)
        #if not len(roles):
        #    try:
        #        return await ctx.send("No roles configured")
        #    except:
        #        pass
        #emb.add_field(
        #    name="Roles:", value="\n".join([ctx.guild.get_role(x).mention for x in roles])
        #)
        #try:
        #    await ctx.send(embed=emb)
        #except discord.Forbidden:
        #    try:
        #        try:
        #            ctx.send("List of roles who will be lockdowned:\n\n".join([ctx.guild.get_role(x).name for x in roles]))
        #        except:
        #            pass
        #    except discord.Forbidden:
        #        pass
        
    async def _lockdown(self, ctx):
        #permissions = discord.Permissions()
        #permissions.update(add_reactions = False)
        #permissions.update(send_messages = False)
        roles = await self._get_block_roles(ctx.guild)
        if not len(roles):
            try:
                return await ctx.send("No roles configured")
            except:
                pass
        else:
            for x in roles:
                role = ctx.guild.get_role(x)
                permissions = role.permissions
                permissions.update(add_reactions = False)
                permissions.update(send_messages = False)
                permissions.update(speak = False)
                try:
                    await ctx.guild.get_role(x).edit(reason = "Lockdown", permissions=permissions)
                except discord.Forbidden:
                    try:
                        await ctx.send("I cannot change the role: " + ctx.guild.get_role(x).name)
                    except:
                        pass

    async def _unlock(self, ctx):
        #permissions = discord.Permissions()
        #permissions.update(add_reactions = True)
        #permissions.update(send_messages = True)
        roles = await self._get_block_roles(ctx.guild)
        if not len(roles):
            try:
                return await ctx.send("No roles configured")
            except:
                pass
        else:
            for x in roles:
                role = ctx.guild.get_role(x)
                permissions = role.permissions
                permissions.update(add_reactions = True)
                permissions.update(send_messages = True)
                permissions.update(speak = True)
                try:
                    await ctx.guild.get_role(x).edit(reason = "Lockdown end", permissions=permissions)
                except discord.Forbidden:
                    try:
                        await ctx.send("I cannot change the role: " + ctx.guild.get_role(x).name)
                    except:
                        pass
            
    async def _add_block_role(self, guild, role):
        async with self.config.guild(guild).blockroles() as rolelist:
            rolelist.append(role)
            
    async def _del_block_role(self, guild, role):
        async with self.config.guild(guild).blockroles() as rolelist:
            rolelist.remove(role)  
    
    async def _get_block_roles(self, guild):
        return await self.config.guild(guild).blockroles()
    
    # permissions = discord.Permissions()
    # permissions.update(kick_members = False)
    # await role.edit(reason = None, colour = discord.Colour.blue(), permissions=permissions, add_reactions=False)