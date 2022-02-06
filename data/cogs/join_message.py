import discord
from discord.ext import commands
from discord.ui import ActionRow, Button, MessageComponents
from discord.enums import ButtonStyle
import discord.interactions


class join_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_dm(self, member):
        guild = self.bot.get_guild(self.bot.guild_id)
        members = guild.member_count
        embed = discord.Embed(title=f"Dobrodošli u FIT Discord, vi ste **{members}.** član. ")
        embed.set_thumbnail(url="https://i.imgur.com/kp1NuMb.png")

        embed.add_field(
            name="Info",
            value="Pravila i informacije možete naći u **welcome** kanalu.\n"
            "Rolove možete dobiti komandama `/roles` ili `/rolovi` u serveru, s kojima dobijate pristup većini kanala.\n"
            "Za sva ostala pitanja možete tagovati moderatore.",
            inline=True,
        )
        embed.set_footer(text="Beep, beep. Ja sam bot.", icon_url="https://i.imgur.com/kp1NuMb.png")
        
        components = MessageComponents(
            ActionRow(
                Button(
                    label="Welcome Kanal",
                    custom_id="url_btn",
                    url="https://discord.com/channels/787773373748740128/792080964121264148/896008582775054336",
                    style=ButtonStyle.link
                ),
                Button(
                    label="Server Invite Link",
                    custom_id="url_btn",
                    url="https://discord.io/FITMostar",
                    style=ButtonStyle.link
                )
            )
        )
        await member.send(embed=embed, components=components)

    # Send DM to member who joins server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_dm(member)

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def admintestdm(self, ctx):
        await ctx.send("DM sent.", ephemeral=True)
        await self.send_dm(ctx.author)


def setup(bot):
    bot.add_cog(join_message(bot))
