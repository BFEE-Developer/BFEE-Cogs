from .bfeeadmin import BFEEAdmin


def setup(bot):
    bot.add_cog(BFEEAdmin(bot))