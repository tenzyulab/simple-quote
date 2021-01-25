from pathlib import Path
from traceback import print_exc

from discord import Game
from discord.ext.commands import (
    BadArgument,
    Bot,
    CheckFailure,
    CommandNotFound,
    when_mentioned_or,
)

import const


class MyBot(Bot):
    def __init__(self):
        super().__init__(command_prefix=when_mentioned_or(const.BOT_PREFIX))
        print(f"{const.BOT_NAME} を起動します。")
        self.remove_command("help")

        for cog in Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"{cog.stem}.pyは正常にロードされました。")
            except Exception:
                print_exc()

    async def on_ready(self):
        print(f"{self.user} としてログインしました。")
        activity = Game(name="/help または @Simple Quote help")
        await self.change_presence(activity=activity)

    async def on_command_error(self, ctx, error):
        ignore_errors = (
            BadArgument,
            CheckFailure,
            CommandNotFound,
        )
        if isinstance(error, ignore_errors):
            return
        await ctx.send(error)


if __name__ == "__main__":
    bot = MyBot()
    bot.run(const.DISCORD_BOT_TOKEN)
