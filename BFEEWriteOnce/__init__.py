from .bfeewriteonce import BFEEWriteOnce


async def setup(bot):
    await bot.add_cog(BFEEWriteOnce(bot))
