import discord
import os
from discord.ext import commands, tasks
import random
import logging
from datetime import datetime

TOKEN = "" # Bot Token
GUILDID = 0 # Guild ID

logging.basicConfig(
    filename=f"data/logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    level=logging.INFO)

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(">>"), help_command=None, intents=intents
)


print(f"Found {len(next(os.walk('data/cogs'))[2])} cogs")
for filename in os.listdir("./data/cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"data.cogs.{filename[:-3]}")
        print(f"  > Loaded {filename[:-3]} [Success]")


@bot.group(invoke_without_command=True)
async def cogs(ctx):
    """
    Return error message if no subcommand is given.
    """
    await ctx.send("Please specify a subcommand.", ephimeral=True)


@commands.has_guild_permissions(manage_guild=True)
@cogs.command()
async def unload(ctx, cog: str):
    """Unloads a cog."""
    cog = cog.lower()
    try:
        bot.unload_extension(f"data.cogs.{cog}")
        await ctx.send(f"Unloaded {cog}", ephemeral=True)
        await update_application_commands()
    except Exception as e:
        await ctx.send(f"Error: {e}", ephemeral=True)


@commands.has_guild_permissions(manage_guild=True)
@cogs.command()
async def load(ctx, cog: str):
    """Loads a cog."""
    cog = cog.lower()
    try:
        bot.load_extension(f"data.cogs.{cog}")
        await ctx.send(f"Loaded {cog}", ephemeral=True)
        await update_application_commands()
    except Exception as e:
        await ctx.send(f"Error: {e}", ephemeral=True)


@commands.has_guild_permissions(manage_guild=True)
@cogs.command()
async def disable(ctx, cog: str):
    """Disables and unloads a cog."""
    cog = cog.lower()
    if not os.path.exists(f"data/cogs/{cog}.py"):
        if os.path.exists(f"data/cogs/{cog}.disabled"):
            return await ctx.send(
                f"`{cog.capitalize()}` is already disabled.", ephemeral=True
            )
        else:
            return await ctx.send(
                f"`{cog.capitalize()}`` is not a cog.", ephemeral=True
            )
    try:
        os.rename(f"data/cogs/{cog}.py", f"data/cogs/{cog}.disabled")
        bot.unload_extension(f"data.cogs.{cog}")
        await ctx.send(f"Disabled `{cog.capitalize()}`", ephemeral=True)
        await update_application_commands()
    except Exception as e:
        if e.__contains__("Cog not loaded"):
            await ctx.send(
                f"`{cog.capitalize()}` wasn't loaded, disabled anyway...",
                ephemeral=True,
            )
        await ctx.send(f"Error: `{e}`", ephemeral=True)


@commands.has_guild_permissions(manage_guild=True)
@cogs.command()
async def enable(ctx, cog: str):
    """Enables and loads a cog."""
    cog = cog.lower()
    if not os.path.exists(f"data/cogs/{cog}.disabled"):
        if os.path.exists(f"data/cogs/{cog}.py"):
            return await ctx.send(
                f"`{cog.capitalize()}`is already enabled.", ephemeral=True
            )
        else:
            return await ctx.send(
                f"`{cog.capitalize()}`` is not a cog.", ephemeral=True
            )
    try:
        os.rename(f"data/cogs/{cog}.disabled", f"data/cogs/{cog}.py")
        bot.load_extension(f"data.cogs.{cog}")
        await ctx.send(f"Enabled `{cog.capitalize()}`", ephemeral=True)
        await update_application_commands()
    except Exception as e:
        print(e)
        await ctx.send(f"`{cog.capitalize()}` is already enabled.", ephemeral=True)


@commands.has_guild_permissions(manage_guild=True)
@cogs.command()
async def reload(ctx, cog: str):
    """Reloads a cog."""
    cog = cog.lower()
    try:
        bot.reload_extension(f"data.cogs.{cog}")
        await ctx.send(f"Reloaded {cog}", ephemeral=True)
        await update_application_commands()
    except Exception as e:
        await ctx.send(f"Error: {e}", ephemeral=True)


@commands.has_guild_permissions(manage_guild=True)
@cogs.command()
async def list(ctx):
    """Lists enabled and disabled cogs separately"""
    enabled_cogs = [
        f"`{i[:-3].capitalize()}`"
        for i in os.listdir("./data/cogs")
        if i.endswith(".py")
    ]
    disabled_cogs = [
        f"`{i[:-9].capitalize()}`"
        for i in os.listdir("./data/cogs")
        if i.endswith(".disabled")
    ]
    message = (
        f"Enabled cogs: {', '.join(enabled_cogs)}\n"
        if enabled_cogs
        else "No enabled cogs.\n"
    )

    message += (
        f"Disabled cogs: {', '.join(disabled_cogs)}"
        if disabled_cogs
        else "No disabled cogs."
    )

    await ctx.send(
        content=message,
        ephemeral=True,
    )


@disable.error
@enable.error
@load.error
@unload.error
@reload.error
@list.error
async def no_permission(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that.", ephemeral=True)


@tasks.loop(seconds=30)
async def status_task():
    await bot.change_presence(
        activity=discord.Game(
            name=f'{random.choice(["discord.io/FITMostar.", "with fire.", "Minecraft.", "with Kez.", "Death Note.", "FIT lmao.", "Destiny", "CS:GO", "VSCode", "C++", "Depression"])}'
        )
    )


async def update_application_commands():
    """
    Checks for a difference between global application (slash)
    commands and the ones used, if there are any, update them.
    """
    gac = await bot.http.get_guild_commands(bot.application_id, GUILDID) # Update guild ID
    gac = {i["name"]: i["description"] for i in gac}
    lac = {i.name: i.help for i in bot.commands}
    if gac != lac:
        print("Updating Application Commands")
        await bot.register_application_commands(commands=None)
        await bot.register_application_commands(guild=bot.get_guild(GUILDID)) # Update guild ID


@bot.event
async def on_ready():
    print("Done loading cogs!")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await update_application_commands()
    print("Bot is ready!")
    status_task.start()


async def main():
    await bot.login(TOKEN)
    await bot.connect()
    bot.loop.run_forever()


loop = bot.loop
loop.run_until_complete(main())
