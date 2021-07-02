import discord
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path

class BFEEAdmin(commands.Cog):
    
    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    # Variables
    default_guild = {
        "blockroles": [],
        "logchannel": "",
        "banned_urls": [
            "stearmcommunnity.ru",
            "stermccommunitty.ru",
            "strearmcomunity.ru",
            "stiemcommunitty.ru",
            "streamcomunnity.ru",
            "streancommunuty.ru",
            "wowcloud9.com",
            "fnaticprize.site",
            "rollskin.ru",
            "ezenze.org",
            "csgocyber.ru",
            "tradeoffers.me",
            "tradeoffers.net.ru",
            "wildday.com",
            "winlems.org.ru",
            "wixzero.pp.ru",
            "seamcommunlty.com",
            "seamcommunty.com",
            "sleamtrade.org.ru",
            "sleamcomnnunity.me",
            "sleamconnunnity.me",
            "sleamcormunity.me",
            "sreancommuniity.com",
            "staemcommeuneuity.ru",
            "staerncomrmunity.com",
            "steaamcomnnunity.com",
            "steaimeecommuniity.com",
            "wowfnatic.com",
            "wowfnatic.site",
            "alexnv.ru",
            "alexandrnav.ru",
            "alexandrs1.ru",
            "ezence.ink",
            "magictop.org.ru",
            "natusvincerytos.org.ru",
            "natusvincerytq.org.ru",
            "natusvincerygivez.xyz",
            "navispot.org.ru",
            "navi.auction",
            "steampromopage.ml",
            "steamcannunlty.com",
            "steamcommanitty.ru",
            "steamcomminiity.site",
            "nvdrop.com",
            "operationbroken.xyz",
            "please.net.ru",
            "rocketcase.xyz",
            "rollcase.com",
            "newgive.com",
            "steamcommnnunnity.world",
            "steamcommnunty.com",
            "steamcommunitycom.xyz",
            "steamcommunlty.comprofilesbloomez.online",
            "steamcommunniitly.ru",
            "stleamconnunltytyztradeoffernewpartnhr15902271.xyz",
            "streamcomnunely.com",
            "tastyskill.net.ru",
            "toomskins.xyz",
            "topgames.org.ru",
            "toprgames.xyz",
            "topwgamez.xyz",
            "topzgames.xyz",
            "golex.org.ru",
            "intimki.com",
            "izinavi.org.ru",
            "linktrade.pp.ua",
            "fnaticwin.xyz",
            "gamstoph.xyz",
            "csmoneiy.us",
            "csgowaycups.org.ru",
            "ezdrop.net.ru",
            "cloud9team.fun",
            "steancomunnity.ru",
            "katowice.ru",
            "cloudteam9.com",
            "streamcommunnlty.ru",
            "stearncomminuty.ru",
            "streammcomunnity.ru",
            "steamcommunytu.ru",
            "streammcomunity.ru",
            "steamcommnuitry.com"
        ]
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
        emb = discord.Embed()
        emb.title = "List of roles who will be lockdowned."
        emb.description = "These roles will be affected by the lockdown command."
        roles = await self._get_block_roles(ctx.guild)
        if not len(roles):
            try:
                return await ctx.send("No roles configured")
            except:
                pass
        emb.add_field(
            name="Roles:", value="\n".join([ctx.guild.get_role(x).mention for x in roles])
        )
        try:
            await ctx.send(embed=emb)
        except discord.Forbidden:
            try:
                try:
                    await ctx.send("```\nList of roles who will be lockdowned:\n\n{}\n```".format("\n".join([ctx.guild.get_role(x).name for x in roles])))
                except:
                    pass
            except discord.Forbidden:
                pass
                
    @commands.group()
    @checks.admin()
    @commands.guild_only()
    async def scam(self, ctx):
        """Scam link settings."""
        pass
        
    @scam.command(name="logchannel")
    @checks.admin()
    @commands.guild_only()
    async def _logchannel(self, ctx, ch: discord.TextChannel = None):
        if not ch:
            return await ctx.send_help()
        await self.config.guild(ctx.guild).logchannel.set(ch.id)    
        await ctx.send("Scam logchannel is now {0}".format(ch.name))
        
    @scam.command(name="addurl")
    @checks.admin()
    @commands.guild_only()
    async def _addurl(self, ctx, url: str = None):
        """Adds url in scamlist."""
        if not url:
            return await ctx.send_help()
        await self._add_scam_url(ctx.guild, url)
        await ctx.send("Added ``{0}`` to scam list".format(url))
        
    @scam.command(name="removeurl")
    @checks.admin()
    @commands.guild_only()
    async def _removeurl(self, ctx, url: str = None):
        """Removes url in scamlist."""
        if not url:
            return await ctx.send_help()
        if url not in await self._get_scam_url(ctx.guild):
            try:
                await ctx.send("URL not in list")
            except:
                pass
        else:        
            await self._del_scam_url(ctx.guild, url)
            await ctx.send("Removed ``{0}`` from scam list".format(url))
        
    #@scam.command(name="listurl")
    #@checks.admin()
    #@commands.guild_only()
    #async def _listurl(self, ctx):
    #    """Lists urls in scamlist."""
    #    emb = discord.Embed()
    #    emb.title = "List of scam URLs."
    #    emb.description = "Messages with one of these urls in them will be removed and reported."
    #    urls = await self._get_scam_url(ctx.guild)
    #    if not len(urls):
    #        try:
    #            return await ctx.send("No URLs configured")
    #        except:
    #            pass
    #    for (let i = 0; i < oldMessage.cleanContent.length; i += 2000) {
    #        const cont = oldMessage.cleanContent.substring(i, Math.min(oldMessage.cleanContent.length, i + 2000));
    #        embed.addField("Old Message", cont);
    #    }
    #    emb.add_field(
    #        name="URLs:", value="\n".join([x for x in urls])
    #    )
    #    try:
    #        await ctx.send(embed=emb)
    #    except discord.Forbidden:
    #        try:
    #            try:
    #                await ctx.send("```\nList of scam URLs.:\n\n{}\n```".format("\n".join([x for x in urls])))
    #            except:
    #                pass
    #        except discord.Forbidden:
    #            pass
                
    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        if message.author.id != self.bot.user.id:
            server = message.guild
            roles = server.roles
            #prole = 816634246009192469 # Kaktus
            prole = 286583179715018752 # BFEE
            role = discord.utils.get(roles, id=prole)
            ctx = await self.bot.get_context(message)
            logchannelid = 246234874011320321 #BFEE
            #logchannelid = 418476587487461377 # Kaktus Test
            
            urls = await self._get_scam_url(ctx.guild)
            
            if len(urls) > 0:
                msg = message
                if any(bannedword in message.content for bannedword in urls):
                    
                    lch = await self.config.guild(ctx.guild).logchannel()
                    if lch is None or lch == "":
                        lch = logchannelid
                        
                    print(lch)
                    ch = self.bot.get_channel(lch)
                    try:
                        await ch.send("The user ``{0}`` sent message ``{1}`` in channel ``{2}``".format(message.author.name, message.content, message.channel))
                    except Exception:
                        pass
                    try:
                        await message.author.add_roles(role, reason="Suspicious message")
                    except Exception:
                        pass
                    try:
                        await message.delete()
                    except Exception:
                        pass
            
    
        
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

    async def _add_scam_url(self, guild, url):
        async with self.config.guild(guild).banned_urls() as banned_urls_list:
            banned_urls_list.append(url)
            
    async def _del_scam_url(self, guild, url):
        async with self.config.guild(guild).banned_urls() as banned_urls_list:
            banned_urls_list.remove(url)
            
    async def _get_scam_url(self, guild):
        return await self.config.guild(guild).banned_urls()
            
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