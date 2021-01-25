from discord.ext.commands import Cog, command


class CogsController(Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            await ctx.send("権限がありません。")
            return False
        return True

    @command(name="load")
    async def _cog_load(self, ctx, cog):
        self.bot.load_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にロードされました。")

    @command(name="unload")
    async def _cog_unload(self, ctx, cog):
        self.bot.unload_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にアンロードされました。")

    @command(name="reload")
    async def _cog_reload(self, ctx, cog):
        self.bot.reload_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にリロードされました。")


def setup(bot):
    bot.add_cog(CogsController(bot))
