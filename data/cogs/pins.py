import discord
from discord.ext import commands
from discord.utils import get
from discord.ui import ActionRow, Button, MessageComponents
from discord.enums import ButtonStyle


class pins(commands.Cog):
    def __init__(self, bot):
        """
        Discord.py cog for pinning messages, made for FIT.
        """
        self.bot = bot
        self.pins_channel_id = 0
        self.pins_channel = None
        self.kez_id = 135754868810973184 # lol

    async def send_to_pins_channel(
        self,
        author,
        author_photo,
        content,
        original_message_link,
        attachments=None,
        embeds=None,
    ):
        """
        Sends a message to the pins channel via webhook.
        """
        if len(content) == 0 and not attachments and not embeds:
            return
        channel = self.bot.get_channel(self.pins_channel_id)
        # Button component for the original message link.
        components = MessageComponents(
            ActionRow(
                Button(
                    label="Original",
                    custom_id="url",
                    url=original_message_link,
                    emoji="🔗",
                    style=ButtonStyle.link,
                )
            )
        )
        if embeds is not None and attachments is None:
            msg = await self.webhook.send(
                content=content if len(content) > 0 else None,
                username=author,
                avatar_url=author_photo,
                components=components,
                embeds=embeds if embeds is not None else None,
                wait=True
            )
            return print(f"[Pins] >> Pinned message {msg}")
        if len(content) > 0 and len(attachments) < 1:
            msg = await self.webhook.send(
                content=content,
                username=author,
                components=components,
                avatar_url=author_photo,
                wait=True
            )
        else:
            msg = await self.webhook.send(
                content=content + "\n" + "\n".join(x.url for x in attachments),
                username=author,
                components=components,
                avatar_url=author_photo,
                wait=True
            )
        print(f"[Pins] >> Pinned message {msg}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Listener for reaction add.
        """
        if payload.emoji.name != "⭐" or payload.channel_id == self.pins_channel_id:
            return
        channel = await self.bot.fetch_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        if isinstance(channel, discord.DMChannel):
            return print("[Pins] DM channel detected.")
        if msg.author.id == self.bot.user.id:
            return print("[Pins] Bot message detected.")
        reaction_validator = get(msg.reactions, emoji="✔️")
        if reaction_validator is not None:
            return print("[Pins] The message was pinned already.")
        reaction = get(msg.reactions, emoji=payload.emoji.name)
        # if reaction is 2 or kez reacted
        if reaction.count == 2 or (payload.user_id == self.kez_id and reaction.count < 2):
            self.pins_channel = await self.bot.fetch_channel(self.pins_channel_id)
            temp_all_webhooks = await self.pins_channel.webhooks()
            self.webhook = temp_all_webhooks[0]
            await self.send_to_pins_channel(
                msg.author.name,
                msg.author.avatar,
                msg.clean_content,
                msg.jump_url,
                msg.attachments,
                msg.embeds,
            )
            print("[Pins] Message sent to pins channel.")
            # Send a DM to the author of the message.
            await msg.author.send(
                "Your message was pinned to the pins channel.\n"
                "You can view it here: <#{}>".format(self.pins_channel_id)
            )
            return await msg.add_reaction("✔️")


def setup(bot):
    bot.add_cog(pins(bot))
