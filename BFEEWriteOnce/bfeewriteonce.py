import aiohttp
import discord
from redbot.core import commands, checks, Config

class BFEEWriteOnce(commands.Cog):
    """BFEEWriteOnce Cog"""
    
    default_guild = {"channels": [], "roles": [] }
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784133733784274, force_registration=True)
        self.config.register_guild(**self.default_guild)
        self.session = aiohttp.ClientSession()
               
    @commands.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def bfeewriteonce(self, ctx):
        """Configuration commands."""
        pass
    
    @bfeewriteonce.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def channel(self, ctx):
        """Configure which channels."""
        pass
        
    @bfeewriteonce.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def role(self, ctx):
        """Configure which role to remove."""
        pass
        
    @role.command(name="add")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _addrole(self, ctx, role: discord.Role = None):
        """Add a role to the list."""
        if role is None:
            await ctx.send("No role specified")
        if role.id not in await self._get_guild_roles(ctx.guild):
            await self._add_guild_role(ctx.guild, role.id)
            await ctx.send("Role added")
        else:
            await ctx.send("Role already added")
    
    @role.command(name="remove")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _removerole(self, ctx, role: discord.Role = None):
        """Remove a role from the list."""
        if role is None:
            await ctx.send("No role specified")
        if role.id not in await self._get_guild_roles(ctx.guild):
            await ctx.send("This role isn't added.")
        else:
            await self._remove_guild_role(ctx.guild, role.id)
            await ctx.send("Role removed")

    @role.command(name="show")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _showrole(self, ctx):
        """Show the list of roles."""
        emb = discord.Embed()
        emb.title = "List of roles configured."
        emb.description = "All things in the world aren't round there are red things too"
        roles = await self._get_guild_roles(ctx.guild)
        if not len(roles):
            return await ctx.send("No roles added")
        emb.add_field(
            name="Roles:", value="\n".join([ctx.guild.get_role(x).mention for x in roles])
        )
        await ctx.send(embed=emb)
        
    @channel.command(name="add")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _addchannel(self, ctx, channel: discord.TextChannel = None):
        """Add a channel to the list."""
        if channel is None:
            channel = ctx.channel
        if channel.id not in await self._get_guild_channels(ctx.guild):
            await self._add_guild_channel(ctx.guild, channel.id)
            await ctx.send("Channel added")
        else:
            await ctx.send("Channel already added")
            
    @channel.command(name="remove")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _removechannel(self, ctx, channel: discord.TextChannel = None):
        """Remove a channel from the list."""
        if channel is None:
            channel = ctx.channel
        if channel.id not in await self._get_guild_channels(ctx.guild):
            await ctx.send("This channel isn't added.")
        else:
            await self._remove_guild_channel(ctx.guild, channel.id)
            await ctx.send("Channel removed")

    @channel.command(name="show")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _showchannel(self, ctx):
        """Show the list of channels."""
        emb = discord.Embed()
        emb.title = "List of channels configured."
        emb.description = "All things in the world aren't round there are red things too"
        channels = await self._get_guild_channels(ctx.guild)
        if not len(channels):
            return await ctx.send("No channels added")
        emb.add_field(
            name="Channels:", value="\n".join([ctx.guild.get_channel(x).mention for x in channels])
        )
        await ctx.send(embed=emb)
        
    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        member = message.author
        server = message.guild
        monitor_channels = await self._get_guild_channels()
        remove_roles = await self._get_guild_roles()
        if member.id == self.bot.user.id:
            return            
        if len(monitor_channels) == 0:
            return
        if message.channel.id not in await self._get_guild_channels(message.author.guild):
            return
        if message.author.guild_permissions.kick_members:
            return
            
        roles = server.roles
        ctx = await self.bot.get_context(message)
        
        try:
            await member.remove_roles(role, reason=("Typed in {chan}").format(chan=message.channel) )
        except discord.Forbidden:
            #await ctx.send(_(GENERIC_FORBIDDEN))
        
    async def _get_guild_channels(self, guild):
        return await self.config.guild(guild).channels()
        
    async def _add_guild_channel(self, guild, channel):
        async with self.config.guild(guild).channels() as chanlist:
            chanlist.append(channel)
            
    async def _remove_guild_channel(self, guild, channel):
        async with self.config.guild(guild).channels() as chanlist:
            chanlist.remove(channel)
            
    async def _get_guild_roles(self, guild):
        return await self.config.guild(guild).roles()
    
    async def _add_guild_role(self, guild, role):
        async with self.config.guild(guild).roles() as rolelist:
            rolelist.append(role)
            
    async def _remove_guild_role(self, guild, role):
        async with self.config.guild(guild).roles() as rolelist:
            rolelist.remove(role)