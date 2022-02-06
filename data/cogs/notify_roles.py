import discord
from discord.ext import commands
from discord.utils import get


class notify_roles(commands.Cog):
    def __init__(self, bot):
        """
        Discord.py cog to notify people.
        """
        self.bot = bot
        self.chosen_roles = ["list", "of", "interger", "ids"]
        
    @commands.has_permissions(administrator=True)
    @commands.command(name="alert")
    async def alert(self, ctx):
        """
        Alert people who haven't picked their roles yet.
        """
        role = get(ctx.guild.roles, id=809189834656317461)
        members = role.members
        members_to_notify = []
        await ctx.send("Checking members...")
        for member in members:
            hasrole = any(role.id in self.chosen_roles for role in member.roles)
            if not hasrole:
                members_to_notify.append(member)
        for member in members_to_notify:
            await member.send("👋 Hello! \nOvu poruku ste dobili jer niste odabrali rolove u FIT serveru, a bez njih ne možete vidjeti većinu kanala.\nMožete ih uzeti s komandom `/roles`, a ako zbog nekog razloga ne želite odabrati godinu ili niste student FIT-a, možete uzeti role **Outsider** sa istom komandom.\nNe planiram ovu poruku slati više puta jer mrzim spam. Lijep pozdrav.")
            print("Sent message to " + member.name)

def setup(bot):
    bot.add_cog(notify_roles(bot))
