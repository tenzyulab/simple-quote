import re

import discord
from discord.ext import commands

pattern = re.compile(
    r"(?<!<)https://(?:(ptb|canary)\.)?discord(app)?\.com/channels/(?P<guild_id>\d+)/(?P<channel_id>\d+)/(?P<message_id>\d+)/?(?!>)")


class Quote(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def create_embed(self, message):
        author = message.author
        embed = discord.Embed(description=message.content,
                              timestamp=message.created_at)
        embed.set_author(name=author.display_name,
                         url=message.jump_url,
                         icon_url=author.avatar_url)
        embed.set_footer(text="#" + message.channel.name)
        return embed

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        response = pattern.finditer(message.content)
        for match_url in response:
            if message.guild.id != int(match_url.group("guild_id")):
                continue
            channel = self.bot.get_channel(int(match_url.group("channel_id")))
            quoted = await channel.fetch_message(int(match_url.group("message_id")))
            embed = await self.create_embed(quoted)
            if quoted.attachments:
                embed.set_image(url=quoted.attachments[0].url)
            await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Quote(bot))
