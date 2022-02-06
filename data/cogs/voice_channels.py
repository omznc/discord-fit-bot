from discord.ext import commands, tasks
from discord import ChannelType

class voice_channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @tasks.loop(minutes=5)
    async def update(self):
        channels = {}
        for channel in self.bot.get_all_channels():
            if " #" in channel.name and channel.type == ChannelType.voice:
                try:
                    int(channel.name.split(" #")[1])
                except ValueError:
                    continue

                name = channel.name.split(" #")[0]
                if channels.get(name) is None:
                    channels[name] = []
                channels[name].append(channel)

        for value in channels.values():
            empty_channels = [channel for channel in value if len(channel.members) == 0]
            
            if not empty_channels:
                to_clone = max(value, key=lambda x: int(x.name.split(" #")[1]))
                name = to_clone.name.split(" #")
                new_channel = await to_clone.clone(
                    name=name[0] + " #" + str(int(name[1]) + 1)
                )
                await new_channel.move(after=to_clone)
                
            if len(empty_channels) > 1:
                to_delete = max(
                    empty_channels, key=lambda x: int(x.name.split(" #")[1])
                )
                await to_delete.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, *args):
        await self.update()


def setup(bot):
    bot.add_cog(voice_channels(bot))
