from glob import glob
from os import getenv
from traceback import print_exc

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class MyBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=commands.when_mentioned_or("/"), **options)
        print("Starting Simple Quote...")

        for cog in [cog.replace("/", ".").replace(".py", "") for cog in glob("cogs/*.py")]:
            try:
                self.load_extension(cog)
                print(f"loaded: {cog}")
            except BaseException:
                print_exc()

    async def on_ready(self):
        user = self.user
        print("logged in as:", str(user))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.BadArgument):
            return
        if isinstance(error, commands.CheckFailure):
            return
        await ctx.send(error)


if __name__ == '__main__':
    bot = MyBot()
    bot.run(getenv("DISCORD_BOT_TOKEN"))
