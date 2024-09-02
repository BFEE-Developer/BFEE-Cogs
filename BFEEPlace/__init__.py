from .bfeeplace import *

async def setup(bot):
    c = BFEEPlace(bot)
    await bot.add_cog(c)