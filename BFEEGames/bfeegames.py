import discord
from .game import Game
from redbot.core import commands, checks, Config
from redbot.core.data_manager import cog_data_path, bundled_data_path

class BFEEGames(commands.Cog):
    
    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "1.0"
    
    hg = Game()
    
    default_guild = {
        "gameleaderrole": "",
        "players": []
    }
      
    def __init__(self, bot):
        self.bot = bot        
        self.config = Config.get_conf(self, identifier=13373427487733784274, force_registration=True)
        self.config.register_guild(**self.default_guild)
        
    @commands.group()
    @commands.guild_only()
    async def bfeegames(self, ctx):
        """BFEE games configuration commands."""
        pass
        
    @bfeegames.command(name="gameleader")
    @checks.admin()
    @commands.guild_only()
    async def _gameleader(self,ctx, role: discord.Role = None):
        self.config.guild(guild).gameleaderrole = role
        
    @bfeegames.command(name="addplayer")
    @commands.guild_only()
    async def _addplayer(self, ctx, user: discord.User = None):
        if not _check_if_gameleader(guild, ctx.author):
            return
        async with self.config.guild(guild).players() as playerlist:
            playerlist.append(user)
            
    @bfeegames.command(name="step")    
    @commands.guild_only()
    async def _step(ctx, *, title: str = None):
        ret = hg.step()
        
        if ret.get('w') is not None:
            e_desc = "The winner is {0} from district {1}!\nWith a total of {2} kills!".format(ret.get('w').name, ret.get('w').district, ret.get('w').kills)
            e_title = "We have the BFEE champion!"
            e_color = 0xd0d645
            e_footer = "Wohoo!"
        elif ret.get('ad') is not None:
            e_desc = "Everyone is dead..\nNone survived..\nThe cleaning crew has started picking up the pieces and are frantically cleaning the trees from blood.\n\nThe BFEE champion will be chosen another day."
            e_title = "Its quiet."
            e_color = 0xd0d645
            e_footer = "Sad day for all"
        else:
            e_desc = ret["messages"]
            e_title = ret["title"]
            e_color = 0xd0d645
            e_footer ret["footer"]       
            
        embed = discord.Embed(title=e_title, color=e_color, description=e_desc)
        embed.set_footer(text=e_footer)
        await ctx.send(embed=embed)
    
    @bfeegames.command(name="startgame")    
    @commands.guild_only()
    async def _new(ctx, *, title: str = None):
        """
        Starts a new Hunger Games in the current channel.
        title - (Optional) The title of the game. Defaults to 'The BFEE Hunger Games'
        """
        if not _check_if_gameleader(guild, ctx.author):
            return
        # Check to see if there are enough players.
        if len(self.config.guild(guild).players()) < 5:
            await ctx.send("There is not enough players, minimum 5")
            return
            
        if title is None or title == "":
            title = "The BFEE Hunger Games"
        else:
            title = _sanitize_all(ctx.message, title)
        owner = ctx.author
        ret = hg.new_game(ctx.channel.id, owner.id, owner.name, title)
        if ret:
            await ctx.send("There is already a game running")
        else:
            hg.start_game(owner, ctx.channel.id, self.config.guild(guild).players())
            
    @bfeegames.command(name="addplayer")    
    @commands.guild_only()
    def _add_player(self, channel_id, user: discord):
        district = math.ceil((len(self.config.guild(guild).players()) + 1) / 2)
        p = Player(name, district)
        
        ret = hg.add_player(ctx.channel.id, name, gender=gender, volunteer=True)
        
        if not this_game.add_player(p):
            return ErrorCode.PLAYER_EXISTS
        gender_symbol = "♂" if is_male else "♀"
        if volunteer:
            return "**District {0} {1} | {2}** volunteers as tribute!".format(p.district, gender_symbol, p.name)
        return "**District {0} {1} | {2}** is selected to be a tribute!".format(p.district, gender_symbol, p.name)
        
    def __strip_mentions(message: discord.Message, text):
        members = message.mentions
        channels = message.channel_mentions
        roles = message.role_mentions

        for m in members:
            name = m.nick if m.nick is not None else m.name
            text = re.sub(m.mention, name, text)
        for c in channels:
            text = re.sub(c.mention, c.name, text)
        for r in roles:
            text = re.sub(r.mention, r.name, text)
        return text
    
    def _sanitize_all(message: discord.Message, text):
        txt = __strip_mentions(message, text)
        txt = __sanitize_here_everyone(txt)
        txt = __sanitize_special_chars(txt)
        return txt
    
    def __sanitize_here_everyone(text):
        text = re.sub('@here', '@\u180Ehere', text)
        text = re.sub('@everyone', '@\u180Eeveryone', text)
        return text
        
    def __sanitize_special_chars(text):
        text = re.sub('@', '\\@', text)
        text = re.sub('~~', '\\~\\~', text)
        text = re.sub('\*', '\\*', text)
        text = re.sub('`', '\\`', text)
        text = re.sub('_', '\\_', text)
        return text.strip()
        
    def _check_if_gameleader(self, guild, user):
        if user.guild_permissions.kick_members:
            return True
        if self.config.guild(guild).gameleaderrole in user.roles:
            return True
        return False