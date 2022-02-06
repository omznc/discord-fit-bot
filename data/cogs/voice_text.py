from discord.ext import commands


class voice_text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_text_channel_id = 0

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        channel = self.bot.get_channel(self.voice_text_channel_id)
        if channel is None:
            channel = await self.bot.fetch_channel(self.voice_text_channel_id)

        if before.channel is None:
            return await channel.set_permissions(member, view_channel=True)
        elif after.channel is None:
            return await channel.set_permissions(member, view_channel=False)


def setup(bot):
    bot.add_cog(voice_text(bot))
