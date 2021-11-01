from .bfeegames import BFEEGames


def setup(bot):
    bot.add_cog(BFEEGames(bot))