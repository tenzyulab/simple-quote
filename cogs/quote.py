import re

import discord
from discord.ext import commands

pattern = re.compile(
    r"(?<!<)https://(?:(ptb|canary)\.)?discord(app)?\.com/channels/(?P<guild_id>\d+)/(?P<channel_id>\d+)/(?P<message_id>\d+)/?(?!>)")


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_copy_embeds(self, embeds, channel):
        for embed in embeds:
            await channel.send(embed=embed)

    async def create_embed(self, message):
        author = message.author
        embed = discord.Embed(description=message.content,
                              timestamp=message.created_at)
        embed.set_author(name=author.display_name,
                         icon_url=author.avatar_url,
                         url=message.jump_url)
        embed.set_footer(text="#" + message.channel.name)
        return embed

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        for match_url in pattern.finditer(message.content):
            if message.guild.id != int(match_url.group("guild_id")):
                continue
            channel = self.bot.get_channel(int(match_url.group("channel_id")))
            quoted = await channel.fetch_message(int(match_url.group("message_id")))

            # If only Embeds are quoted
            if len(quoted.content) == 0 and quoted.embeds:
                await self.send_copy_embeds(quoted.embeds, channel)
                continue

            # If quoted from NSFW to SFW
            if channel.is_nsfw() and not message.channel.is_nsfw():
                quoted.content = "**Quoted from NSFW**\nclick to view messageUrl"
                quoted.attachments = None
            embed = await self.create_embed(quoted)

            # if quoted Image
            fixed_file = None
            if quoted.attachments:
                if quoted.attachments[0].is_spoiler():
                    fixed_file = await quoted.attachments[0].to_file(spoiler=True)
                else:
                    embed.set_image(url=quoted.attachments[0].url)
            
            await message.channel.send(embed=embed, file=fixed_file)

            # If embeds are also quoted
            if quoted.embeds:
                await message.channel.send("──────────")
                await self.send_copy_embeds(quoted.embeds, channel)

def setup(bot):
    bot.add_cog(Quote(bot))
