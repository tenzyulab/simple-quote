from discord.ext import commands


class Mod(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not await ctx.bot.is_owner(ctx.author):
            await ctx.send("権限がありません。")
            return False
        return True

    @commands.command(name="load")
    async def owner_load(self, ctx, cog):
        self.bot.load_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にロードされました。")

    @commands.command(name="unload")
    async def owner_unload(self, ctx, cog):
        self.bot.unload_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にアンロードされました。")

    @commands.command(name="reload")
    async def owner_reload(self, ctx, cog):
        self.bot.reload_extension("cogs." + cog)
        await ctx.send(f"{cog}.pyは正常にリロードされました。")


def setup(bot):
    bot.add_cog(Mod(bot))
