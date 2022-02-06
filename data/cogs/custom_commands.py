from discord import Embed, embeds
from discord.ext import commands
import json


class custom_commands(commands.Cog):
    def __init__(self, bot):
        """
        Discord.py cog for creating simple user commands on the fly.
        """
        self.bot = bot
        self.commands_dict = {
            k: v
            for k, v in sorted(
                json.load(open("data/commands.json")).items(),
                key=lambda item: item[1]["uses"],
                reverse=True,
            )
        }
        numberofcommands = len(self.commands_dict)
        print(
            f"  > Loading commands [Waiting]\n\t  > Found {numberofcommands} command{'s' if numberofcommands > 1 or numberofcommands == 0 else ''}"
        )
        for command, command_dict in self.commands_dict.items():
            self.bot.add_command(
                commands.Command(
                    name=command,
                    func=self.usercommand,
                    help=command_dict["description"],
                )
            )

    async def usercommand(self, ctx):
        """
        Figures out what reply to send from the ctx context and sending it.
        """
        await ctx.send(self.commands_dict[str(ctx.command)]["reply"])
        self.commands_dict[ctx.command.name]["uses"] += 1
        self.commands_dict = {
            k: v
            for k, v in sorted(
                self.commands_dict.items(),
                key=lambda item: item[1]["uses"],
                reverse=True,
            )
        }
        json.dump(self.commands_dict, open("data/commands.json", "w"), indent=4)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def add(self, ctx, name, reply, description):
        """
        Add a new command, administrator-only.
        """
        # Check if the command exists
        if name in self.commands_dict:
            return await ctx.send("That command already exists!")

        self.commands_dict[name] = {
            "description": description,
            "uses": 0,
            "reply": reply,
        }
        self.bot.add_command(
            commands.Command(name=name, func=self.usercommand, help=description)
        )
        json.dump(self.commands_dict, open("data/commands.json", "w"), indent=4)
        await ctx.send(f"Command {name} added. It will appear soon.", ephemeral=True)
        tbd = await self.bot.http.get_guild_commands(
            self.bot.application_id, self.bot.guild_id
        )
        for command in tbd:
            await self.bot.http.delete_guild_command(
                self.bot.application_id, self.bot.guild_id, command["id"]
            )
        await self.bot.register_application_commands(
            guild=self.bot.get_guild(self.bot.guild_id)
        )

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def edit(self, ctx, name, reply):
        """
        Edit a command, administrator-only.
        """

        if name not in self.commands_dict:
            return await ctx.send("Command not found!", ephemeral=True)

        self.commands_dict[name]["reply"] = reply

        json.dump(self.commands_dict, open("data/commands.json", "w"), indent=4)
        return await ctx.send("Command edited!", ephemeral=True)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def remove(self, ctx, name):
        """
        Remove a command, administrator-only.
        """

        if name not in self.commands_dict:
            return await ctx.send("Command not found!", ephemeral=True)

        self.bot.remove_command(name)
        del self.commands_dict[name]

        await ctx.send("Command will be removed shortly!", ephemeral=True)
        commands = await self.bot.http.get_guild_commands(
            self.bot.application_id, self.bot.guild_id
        )

        json.dump(self.commands_dict, open("data/commands.json", "w"), indent=4)

        for command in commands:
            if command["name"] == name:
                await self.bot.http.delete_guild_command(
                    self.bot.application_id, self.bot.guild_id, command["id"]
                )

    @commands.command()
    async def list(self, ctx):
        """
        List the existing commands.
        """
        page = 1
        page_size = int(len(self.commands_dict) / 20)
        embed = await self.setupembed(page=page, page_size=page_size)
        for fields, command in enumerate(self.commands_dict):
            if fields != 0 and fields % 20 == 0:
                await ctx.send(embed=embed, ephemeral=True)
                page += 1
                embed = await self.setupembed(page=page, page_size=page_size)
            embed.add_field(
                name=f"__{command.capitalize()}__",
                value=f'{self.commands_dict[command]["description"]}',
                inline=True,
            )
        return await ctx.send(embed=embed, ephemeral=True)

    async def setupembed(self, page, page_size):
        embed = Embed(title=f"Lista Komandi ({page}/{page_size+1})", color=0x00FFFF)
        embed.set_thumbnail(url="https://i.imgur.com/Ogtw9Xo.png")
        embed.set_footer(text="https://discord.io/FITMostar")
        return embed

    @edit.error
    @add.error
    @remove.error
    async def not_admin_error(self, ctx, error):
        """
        Method that handles interactions with non administrators for the help command.
        """
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send("This command is only for administrators.", ephemeral=True)


def setup(bot):
    bot.add_cog(custom_commands(bot))
