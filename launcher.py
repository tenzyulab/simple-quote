import glob
from os import getenv
from pathlib import Path
from traceback import print_exc

from discord.ext import commands


class MyBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=commands.when_mentioned_or("/"), **options)
        print("Starting Simple Quote...")
        self.remove_command("help")

        for cog in Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"Loaded {cog.stem}.py")
            except:
                print_exc()

    async def on_ready(self):
        print("logged in as:", self.user.name, self.user.id)

    async def on_command_error(self, ctx, error):
        ignore_errors = (
            commands.CommandNotFound,
            commands.BadArgument,
            commands.CheckFailure,
        )
        if isinstance(error, ignore_errors):
            return
        await ctx.send(error)


if __name__ == "__main__":
    bot = MyBot()
    bot.run(getenv("DISCORD_BOT_TOKEN"))
