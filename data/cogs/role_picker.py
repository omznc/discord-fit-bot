from asyncio import TimeoutError
from discord.ext import commands
from discord.enums import ButtonStyle
from discord.ext.commands.core import defer
from discord.ui import ActionRow, Button, MessageComponents
from discord import PartialEmoji
import time


class role_picker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.year_roles = [
            864476634765197322,
            864476671080136724,
            874644619164520468,
            874644721522319410,
            830499512086822912,
        ]

    def get_game_row(self, author_roles: list[int], row: int):
        if row == 1:
            return ActionRow(
                Button(
                    label="Jackbox Party Pack",
                    custom_id="787773373748740133",
                    emoji=PartialEmoji(name="jackbox", id="794193504640303116"),
                    style=ButtonStyle.green
                    if 787773373748740133 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Among Us",
                    custom_id="787773373769580605",
                    emoji=PartialEmoji(name="amongus", id="794193504255344651"),
                    style=ButtonStyle.green
                    if 787773373769580605 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Destiny 2",
                    custom_id="848273347908993024",
                    emoji=PartialEmoji(name="Destiny", id="848273546106109972"),
                    style=ButtonStyle.green
                    if 848273347908993024 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Minecraft",
                    custom_id="816253757381804052",
                    emoji=PartialEmoji(name="minecraft", id="816254096319316028"),
                    style=ButtonStyle.green
                    if 816253757381804052 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Overwatch",
                    custom_id="818119579909357598",
                    emoji=PartialEmoji(name="overwatch", id="818119428096524348"),
                    style=ButtonStyle.green
                    if 818119579909357598 in author_roles
                    else ButtonStyle.secondary,
                ),
            )
        elif row == 2:
            return ActionRow(
                Button(
                    label="League of Legends",
                    custom_id="800449687814406189",
                    emoji=PartialEmoji(name="league", id="800449948717809704"),
                    style=ButtonStyle.green
                    if 800449687814406189 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Grand Theft Auto V",
                    custom_id="787773373748740132",
                    emoji=PartialEmoji(name="gtav", id="794206339265986610"),
                    style=ButtonStyle.green
                    if 787773373748740132 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Star Wars: Battlefront II ",
                    custom_id="799312217089900574",
                    emoji=PartialEmoji(name="vader", id="799314233007276032"),
                    style=ButtonStyle.green
                    if 799312217089900574 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Counter Strike: Global Offensive",
                    custom_id="787773373769580604",
                    emoji=PartialEmoji(name="csgo", id="794193504782778368"),
                    style=ButtonStyle.green
                    if 787773373769580604 in author_roles
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="PLAYERUNKNOWN'S BATTLEGROUNDS",
                    custom_id="929053434311741521",
                    emoji=PartialEmoji(name="pubg", id="929053846326624338"),
                    style=ButtonStyle.green
                    if 929053434311741521 in author_roles
                    else ButtonStyle.secondary,
                ),
            )
        else:
            return ActionRow(
                Button(
                    label="VALORANT",
                    custom_id="929056368420347946",
                    emoji=PartialEmoji(name="VALORANT", id="929056331170713610"),
                    style=ButtonStyle.green
                    if 929056368420347946 in author_roles
                    else ButtonStyle.secondary,
                )
            )

    def get_functionality_row(self, author_roles: list[int]):
        return ActionRow(
            Button(
                label="DLWMS",
                custom_id="796116996000579644",
                emoji="📢",
                style=ButtonStyle.green
                if 796116996000579644 in author_roles
                else ButtonStyle.secondary,
            ),
            Button(
                label="Voice Chat",
                custom_id="799312445952753704",
                emoji="🎙️",
                style=ButtonStyle.green
                if 799312445952753704 in author_roles
                else ButtonStyle.secondary,
            ),
            Button(
                label="Free Games",
                custom_id="799312367405891595",
                emoji="🎮",
                style=ButtonStyle.green
                if 799312367405891595 in author_roles
                else ButtonStyle.secondary,
            ),
        )

    def get_years_row(self, author_roles: list[int]):
        return ActionRow(
            Button(
                label="Outsider",
                custom_id="830499512086822912",
                emoji="🕹",
                style=ButtonStyle.green
                if 830499512086822912 in author_roles
                else ButtonStyle.secondary,
            ),
            Button(
                label="Prva Godina",
                custom_id="864476634765197322",
                emoji="1️⃣",
                style=ButtonStyle.green
                if 864476634765197322 in author_roles
                else ButtonStyle.secondary,
            ),
            Button(
                label="Druga Godina",
                custom_id="864476671080136724",
                emoji="2️⃣",
                style=ButtonStyle.green
                if 864476671080136724 in author_roles
                else ButtonStyle.secondary,
            ),
            Button(
                label="Treca Godina",
                custom_id="874644619164520468",
                emoji="3️⃣",
                style=ButtonStyle.green
                if 874644619164520468 in author_roles
                else ButtonStyle.secondary,
            ),
            Button(
                label="Cetvrta Godina",
                custom_id="874644721522319410",
                emoji="4️⃣",
                style=ButtonStyle.green
                if 874644721522319410 in author_roles
                else ButtonStyle.secondary,
            ),
        )

    def get_components(self, author_roles: list[int], role_toggle=None):
        if role_toggle is None or role_toggle not in self.year_roles:
            return MessageComponents(
                self.get_years_row(author_roles),
                self.get_functionality_row(author_roles),
                self.get_game_row(author_roles, 1),
                self.get_game_row(author_roles, 2),
                self.get_game_row(author_roles, 3)
            )
        return MessageComponents(
            ActionRow(
                Button(
                    label="Outsider",
                    custom_id="830499512086822912",
                    emoji="🕹",
                    style=ButtonStyle.green
                    if role_toggle == 830499512086822912
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Prva Godina",
                    custom_id="864476634765197322",
                    emoji="1️⃣",
                    style=ButtonStyle.green
                    if role_toggle == 864476634765197322
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Druga Godina",
                    custom_id="864476671080136724",
                    emoji="2️⃣",
                    style=ButtonStyle.green
                    if role_toggle == 864476671080136724
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Treca Godina",
                    custom_id="874644619164520468",
                    emoji="3️⃣",
                    style=ButtonStyle.green
                    if role_toggle == 874644619164520468
                    else ButtonStyle.secondary,
                ),
                Button(
                    label="Cetvrta Godina",
                    custom_id="874644721522319410",
                    emoji="4️⃣",
                    style=ButtonStyle.green
                    if role_toggle == 874644721522319410
                    else ButtonStyle.secondary,
                ),
            ),
            self.get_functionality_row(author_roles),
            self.get_game_row(author_roles, 1),
            self.get_game_row(author_roles, 2),
        )

    async def role_backend(self, ctx):
        guild = await self.bot.fetch_guild(787773373748740128)
        author_roles = [int(role.id) for role in ctx.author.roles]
        base_components = self.get_components(author_roles=author_roles)
        msg = await ctx.send(
            "Odaberite rolove // Choose your roles (60s)",
            components=base_components,
            ephemeral=True,
        )

        t_end = time.time() + 60
        while time.time() < t_end:
            try:
                interaction = await self.bot.wait_for(
                    "component_interaction", timeout=60, check=lambda c: c.user == ctx.author
                )
            except TimeoutError:
                return await msg.edit(
                    content="Isteklo vrijeme // Timed out", components=None
                )
            if time.time() > t_end:
                return await msg.edit(
                    content="Isteklo vrijeme // Timed out", components=None
                )
            if int(interaction.component.custom_id) in self.year_roles:
                for role in self.year_roles:
                    try:
                        author_roles.remove(role)
                        await ctx.author.remove_roles(guild.get_role(role))
                    except ValueError:
                        pass
                await ctx.author.add_roles(
                    guild.get_role(int(interaction.component.custom_id))
                )
                author_roles.append(int(interaction.component.custom_id))
            else:
                try:
                    author_roles.remove(int(interaction.component.custom_id))
                    await ctx.author.remove_roles(
                        guild.get_role(int(interaction.component.custom_id))
                    )
                except ValueError:
                    await ctx.author.add_roles(
                        guild.get_role(int(interaction.component.custom_id))
                    )
                    author_roles.append(int(interaction.component.custom_id))

            comp = self.get_components(
                author_roles=author_roles,
                role_toggle=int(interaction.component.custom_id),
            )
            await msg.edit(components=comp)
            await interaction.response.defer_update()

    @commands.command()
    async def roles(self, ctx: commands.Context):
        """Pick a role, any role..."""
        await self.role_backend(ctx)

    @commands.command()
    async def rolovi(self, ctx: commands.Context):
        """Pick a role, any role..."""
        await self.role_backend(ctx)


def setup(bot):
    bot.add_cog(role_picker(bot))
