from .bfeewriteonce import BFEEWriteOnce


def setup(bot):
    bot.add_cog(BFEEWriteOnce(bot))
