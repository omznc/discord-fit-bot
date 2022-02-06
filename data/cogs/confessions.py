from discord.ext import commands
from discord.utils import escape_mentions
import aiohttp
from discord import Webhook


class confessions(commands.Cog):
    def __init__(self, bot):
        """
        Confessions - The cog!
        """
        self.bot = bot
        self.confessions_channel_id = 0
        self.confessions_webhook_url = ""
        self.confessions_user_avatar_url = ""

    @commands.command()
    async def confess(self, ctx, confession):
        """
        Publically, but anonymously, confess something. Do /confess help for more info.
        """
        if confession == "help":
            return await ctx.send(
                f"Whatever you send to the command will be sent to <#{self.confessions_channel_id}>\
                \nI do not keep records on who sends what, and there is no way of me knowing who sent what.\
                \n**I never plan on changing that**\
                \nOther people can reply to your confession, but if you never respond they will never know who it was\
                \n__Could just be general advice, mockery, personal experiences, etc.__\
                \nThat's it, have fun.",
                ephemeral=True,
            )
        elif confession == "source":
            return await ctx.send(
                "https://go.poseri.ga/confessions-source-code", ephemeral=True
            )
        await ctx.send(
            content=f"Your confession has been sent to <#{self.confessions_channel_id}>\
            \n_This message is only seen by you, and not even I keep records on who you are_",
            ephemeral=True,
        )
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(self.confessions_webhook_url, session=session)
            content = f"{confession}"
            sent_webhook_temp = await webhook.send(
                username="An Anonymous Member",
                content=escape_mentions(content),
                avatar_url=self.confessions_user_avatar_url,
                wait=True,
            )
            msg = await self.bot.get_channel(self.confessions_channel_id).fetch_message(
                sent_webhook_temp.id
            )
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            await msg.add_reaction("😢")
            await msg.add_reaction("😂")


def setup(bot):
    bot.add_cog(confessions(bot))
