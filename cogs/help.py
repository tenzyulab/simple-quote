from textwrap import dedent

from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            dedent(
                """\
            # Simple Quote は Discord のメッセージの引用をサポートする bot です。

            # 使い方
            メッセージに引用したいメッセージのURLを含めるだけです。
            埋め込みリンクを展開したくない場合は、標準機能と同様にURLを < > で囲んでください。

            # GitHubはこちら
            <https://github.com/tenzyu/simple-quote>

            # サポートサーバーはこちら
            <https://discord.gg/4nSKCE9RRn>
            """
            )
        )


def setup(bot):
    bot.add_cog(Help(bot))
