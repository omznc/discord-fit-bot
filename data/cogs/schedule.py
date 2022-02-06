from discord.ext import commands
import json
from discord.ui import (
    MessageComponents,
    Button,
    ButtonStyle,
    ActionRow,
    SelectMenu,
    SelectOption,
)


class schedule(commands.Cog):
    def __init__(self, bot):
        """
        Discord.py cog for sending the schedule.
        """
        self.bot = bot
        self.year_roles = {
            "first": 0,
            "second": 0,
            "third": 0,
            "fourth": 0,
        } # IDS
        # load data/rasporedi.json as dict self.schedules
        with open("data/rasporedi.json", "r") as f:
            self.schedules = json.load(f)

    @commands.command()
    async def raspored(self, ctx):
        # Check if user has any of the self.year_roles
        # Save all user's roles to a list
        user_roles = [role.id for role in ctx.author.roles]
        year = None
        if all(role not in self.year_roles.values() for role in user_roles):
            msg = await ctx.send(
                "Niste odabrali godinu (`/rolovi` ili `/roles`). Koji raspored želite? (60s)",
                components=MessageComponents(
                    ActionRow(
                        Button(
                            label="In-Class",
                            custom_id="inclass",
                            emoji="🏫",
                            style=ButtonStyle.green,
                        ),
                        Button(
                            label="DL",
                            custom_id="dl",
                            emoji="💻",
                            style=ButtonStyle.green,
                        ),
                    )
                ),
                ephemeral=True,
            )
            try:
                interaction = await self.bot.wait_for(
                    "component_interaction",
                    check=lambda c: c.user == ctx.author,
                    timeout=60,
                )
            except:
                return await msg.edit(
                    content="Vrijeme je isteklo. Pokušajte ponovno.", components=None
                )
            await interaction.response.defer_update()
            metoda = interaction.component.custom_id
            await msg.edit(
                content="Niste odabrali godinu (`/rolovi` ili `/roles`). Koji raspored želite? (60s)",
                components=MessageComponents(
                    ActionRow(
                        SelectMenu(
                            options=[
                                SelectOption(
                                    label=value.get("name"),
                                    value=key,
                                    emoji=value.get("emoji"),
                                )
                                for key, value in self.schedules.get(
                                    interaction.component.custom_id
                                ).items()
                            ],
                            custom_id="share_selection",
                            min_values=1,
                            max_values=1,
                        )
                    ),
                ),
            )
            try:
                interaction = await self.bot.wait_for(
                    "component_interaction",
                    check=lambda c: c.user == ctx.author,
                    timeout=60,
                )
            except:
                return await msg.edit(
                    content="Vrijeme je isteklo. Pokušajte ponovno.", components=None
                )
            print(metoda)
            await interaction.response.defer_update()
            subdir = self.schedules.get(metoda).get(str(interaction.values[0]))
        else:
            for role in self.year_roles.keys():
                if self.year_roles[role] in user_roles:
                    year = self.year_roles[role]
                    break

            # Figure out which role id corresponse to year_roles
            for key, value in self.year_roles.items():
                if value == year:
                    year = key
                    break

            # Send 2 buttons to choose between inclass and dl
            msg = await ctx.send(
                content="In-Class ili DL? (60s)",
                components=MessageComponents(
                    ActionRow(
                        Button(
                            label="In-Class",
                            custom_id="inclass",
                            emoji="🏫",
                            style=ButtonStyle.green,
                        ),
                        Button(
                            label="DL",
                            custom_id="dl",
                            emoji="💻",
                            style=ButtonStyle.green,
                        ),
                    )
                ),
                ephemeral=True,
            )

            # Wait for user to click on one of the buttons
            try:
                interaction = await self.bot.wait_for(
                    "component_interaction",
                    check=lambda c: c.user == ctx.author,
                    timeout=60,
                )
            except:
                return await msg.edit(
                    content="Vrijeme za odabir rolova je isteklo. Pokušajte ponovno.", components=None
                )
            await interaction.response.defer_update()
            subdir = self.schedules.get(interaction.component.custom_id).get(year)
            if subdir is None:
                return print("Error in getting subdir")

        return await msg.edit(
            content=subdir.get("name") + "\n" + subdir.get("url"),
            components=None,
        )


def setup(bot):
    bot.add_cog(schedule(bot))
