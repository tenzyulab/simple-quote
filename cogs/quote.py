import re

import discord
from discord.ext import commands

pattern = re.compile(
    r"(?<!<)https://(?:(ptb|canary)\.)?discord(app)?\.com/channels/(?P<guild_id>\d+)/(?P<channel_id>\d+)/(?P<message_id>\d+)/?(?!>)"
)


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_copied_embeds(self, embeds, channel):
        for embed in embeds:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        for match_url in pattern.finditer(message.content):
            if message.guild.id != int(match_url.group("guild_id")):
                continue
            channel = self.bot.get_channel(int(match_url.group("channel_id")))
            quoted = await channel.fetch_message(int(match_url.group("message_id")))

            # If quoted from NSFW to SFW
            if channel.is_nsfw() and not message.channel.is_nsfw():
                embed = discord.Embed(
                    title="**Quoted from NSFW**",
                    url=quoted.jump_url,
                    description="click to view messageUrl",
                    timestamp=quoted.created_at,
                )
                embed.set_footer(text="#NSFW")
                await message.channel.send(embed=embed)
                continue

            # If no messages
            if len(quoted.content) == 0:
                if quoted.attachments:
                    if quoted.attachments[0].is_spoiler():
                        fixed_file = await quoted.attachments[0].to_file(spoiler=True)
                        await message.channel.send(file=fixed_file)
                    else:
                        embed = discord.Embed()
                        embed.set_image(url=quoted.attachments[0].url)
                        await message.channel.send(embed=embed)
                if quoted.embeds:
                    await self.send_copied_embeds(quoted.embeds, message.channel)
                continue

            embed = discord.Embed(
                description=quoted.content, timestamp=quoted.created_at
            )
            embed.set_author(
                name=quoted.author.display_name,
                icon_url=quoted.author.avatar_url,
                url=quoted.jump_url,
            )

            fixed_file = None
            if quoted.attachments:
                if quoted.attachments[0].is_spoiler():
                    fixed_file = await quoted.attachments[0].to_file(spoiler=True)
                else:
                    embed.set_image(url=quoted.attachments[0].url)

            await message.channel.send(embed=embed, file=fixed_file)

            if quoted.embeds:
                await message.channel.send("────────")
                await self.send_copied_embeds(quoted.embeds, message.channel)


def setup(bot):
    bot.add_cog(Quote(bot))
