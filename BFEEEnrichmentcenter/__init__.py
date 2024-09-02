from .bfeeenrichmentcenter import BFEEEnrichmentCenter

async def setup(bot):
    c = BFEEEnrichmentCenter(bot)
    await bot.add_cog(c)