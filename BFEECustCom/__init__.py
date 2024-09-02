from .bfeecustcom import BFEECustomCommands

async def setup(bot):
    c = BFEECustomCommands(bot)
    await bot.add_cog(c)
