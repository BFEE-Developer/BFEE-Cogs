from .bfeegiveaway import BFEEGiveaway


def setup(bot):
    bot.add_cog(BFEEGiveaway(bot))