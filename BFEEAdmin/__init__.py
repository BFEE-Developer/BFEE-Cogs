from .bfeeadmin import BFEEAdmin

async def setup(bot):
    c = BFEEAdmin(bot)
    await bot.add_cog(c)