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
    async def roles(self, ctx):
        """Configure which role to remove."""
        pass
        
    @channel.command(name="add")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _add(self, ctx, channel: discord.TextChannel = None):
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
    async def _remove(self, ctx, channel: discord.TextChannel = None):
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
    async def _show(self, ctx):
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
        
    async def _get_guild_channels(self, guild):
        return await self.config.guild(guild).channels()
        
    async def _add_guild_channel(self, guild, channel):
        async with self.config.guild(guild).channels() as chanlist:
            chanlist.append(channel)
            
    async def _remove_guild_channel(self, guild, channel):
        async with self.config.guild(guild).channels() as chanlist:
            chanlist.remove(channel)