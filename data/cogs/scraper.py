from discord.ext import tasks, commands
from discord.ui import ActionRow, Button, MessageComponents
from discord.enums import ButtonStyle
from bs4 import BeautifulSoup
import html2md
from datetime import datetime
import requests
import praw
import discord
import json
import os

thumbnail = channelID = guild_id = webhook_url = roleTagID = statuses = sleepInSeconds = post_to_reddit = fiturl = headers = data = avatars = redditdata = None
try:
    config = open("data/config.json")
except FileNotFoundError:
    print("ERROR: The config.json not accessible. Check README.md")
    exit()
finally:
    config = json.load(config)
    globals().update(config)

# Post to Subreddit too.
reddit = praw.Reddit(
    client_id=redditdata["client_id"],
    client_secret=redditdata["client_secret"],
    password=redditdata["password"],
    user_agent=redditdata["user_agent"],
    username=redditdata["username"],
    check_for_async=False,
)
reddit.validate_on_submit = True
bot = reddit.redditor(redditdata["username"])
print(
    f"  > Loading scraper [Waiting]\n\t  > Posting to Reddit: {'Enabled' if post_to_reddit else 'Disabled'}"
)

# Check if URL is valid
async def is_url(url):
    try:
        requests.get(f"https://{url}/student")
        return True
    except Exception as e:
        print(f"Error in checking url {url}: {e}")
        return False


class scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.guild_id = guild_id
        self.background.start()
        self.runs = 0
        self.bot.statuses = statuses

    async def get_dynamic_header_data(self):
        global data, fiturl
        with requests.Session() as r:
            r = r.get(f"https://{fiturl}/student/login.aspx")
            soup = BeautifulSoup(r.text, "lxml")
            data["__VIEWSTATE"] = soup.find("input", {"id": "__VIEWSTATE"})["value"]
            data["__VIEWSTATEGENERATOR"] = soup.find(
                "input", {"id": "__VIEWSTATEGENERATOR"}
            )["value"]
            data["__EVENTVALIDATION"] = soup.find("input", {"id": "__EVENTVALIDATION"})[
                "value"
            ]

    async def get_title(self):
        global fiturl
        with requests.Session() as s:
            s.post(f"https://{fiturl}/student/login.aspx", headers=headers, data=data)
            s = s.get(f"https://{fiturl}/student/default.aspx")
            soup = BeautifulSoup(s.text, "lxml")
            _title = soup.find("a", {"id": "lnkNaslov"})
            # Checks if there is a description preview.
            try:
                short_description = soup.find("div", {"class": "abstract"}).text
            except:
                short_description = False
            return _title.text.strip(), _title, short_description

    async def check_if_post_exists(self, title, channel):
        old_embed = None
        messages = await channel.history(limit=10).flatten()
        for msg in messages:
            embeds = msg.embeds
            if embeds is None:
                continue
            for embed in embeds:
                old_embed = embed.to_dict()
                if old_embed.get("title") == title:
                    return False
        return True

    async def get_details(self, article_url):
        with requests.Session() as o:
            o.post(
                f"https://{fiturl}/student/login.aspx",
                headers=headers,
                data=data,
            )
            o = o.get(article_url)
        soup = BeautifulSoup(o.text, "lxml")
        try:
            content = "".join(
                i.text for i in soup.find("div", {"id": "Panel1"}).find_all("p")
            )
        except:
            content = False
        author = soup.find("a", {"id": "linkNapisao"}).text
        date = soup.find("span", {"id": "lblDatum"}).text

        # Some fancy date formatting and OS checking.
        if os.name == "nt":
            date = datetime.strptime(date, "%d.%m.%Y %H:%M -").strftime(
                "%#d. %B, %Y at %H:%M"
            )
        else:
            date = datetime.strptime(date, "%d.%m.%Y %H:%M -").strftime(
                "%-d. %B, %Y at %H:%M"
            )

        return content, author, date

    async def make_embed(self, postData):
        notext = False
        if not postData["content"]:
            noPostDescription = (
                "Obavijest nema teksta. Kliknite na naslov da otvorite u browser-u."
            )
            embed = discord.Embed(
                title=postData["title"],
                url=postData["article_url"],
                description=noPostDescription,
                color=0xF6F6F6,
            )
            notext = True
        elif len(postData["content"]) > 2000:
            if "short_description" != False:
                description = f"{postData['short_description']} \n\nPoruka preduga. Otvorite u browseru."
            else:
                description = "\n\nPoruka preduga. Otvorite u browseru."

            embed = discord.Embed(
                title=postData["title"],
                url=postData["article_url"],
                description=description,
                color=0xF6F6F6,
            )
        else:
            embed = discord.Embed(
                title=postData["title"],
                url=postData["article_url"],
                description=postData["content"],
                color=0xF6F6F6,
            )

        return notext, embed

    @tasks.loop(minutes=5)
    async def background(self):
        global data, headers, channelID, fiturl
        if not await is_url(fiturl):
            fiturl = "fit.unmo.ba"
            print(f"Changed URL to {fiturl}")
        await self.bot.wait_until_ready()
        channel = await self.bot.fetch_channel(channelID)
        try:
            self.runs += 1
            await self.get_dynamic_header_data()
            # Logs in and gets the title and short description
            title, _title, short_description = await self.get_title()
            if await self.check_if_post_exists(title, channel):
                article_url = f"https://{fiturl}/student/{_title['href']}"
                content, author, date = await self.get_details(article_url)

                # I didn't want to rewrite the code to adapt it to BS4, so I just kept it as a dict.
                postData = {
                    "content": content,
                    "title": title,
                    "author": author,
                    "article_url": article_url,
                    "short_description": short_description,
                    "date": date,
                }
                notext = False

                # This basically makes the bot do things.
                notext, embed = await self.make_embed(postData)

                author = postData["author"].split()[0]
                icon = avatars[author] if author in avatars else avatars["default"]
                # Attribution. Please keep it here, thanks.
                embed.set_footer(
                    text=f"Posted on {postData['date']}  |  /roles za @DLWMS"
                )

                if thumbnail:
                    embed.set_thumbnail(url=thumbnail)

                webhook = await channel.webhooks()
                webhook = webhook[0]

                await webhook.send(
                    content="<@&796116996000579644>",
                    embed=embed,
                    username=postData["author"],
                    avatar_url=icon,
                    components=MessageComponents(
                        ActionRow(
                            Button(
                                label="Original",
                                custom_id="url_btn",
                                url=postData["article_url"],
                                emoji="📰",
                                style=ButtonStyle.link,
                            ),
                            Button(
                                label="FIT Discord",
                                custom_id="url_btn",
                                url="https://discord.io/FITMostar",
                                emoji="🧑‍🤝‍🧑",
                                style=ButtonStyle.link,
                            )
                        )
                    ),
                )

                print("Message succesfully sent to discord >> " + postData["title"])
                self.post_to_reddit(postData, notext)
                print("Reddit posted >> " + postData["title"])

        except Exception as e:
            print(f"[{self.runs}] Failed with Exception {e}.")

    def post_to_reddit(self, postData, notext):
        if post_to_reddit:
            if notext:
                reddit.subreddit("FITMostar").submit(
                    f'{postData["title"]} | {postData["author"]}',
                    url=postData["article_url"],
                    flair_id="f7b632d0-cd25-11eb-9037-0e1440c58fd5",
                )
                print("Posted notext")
            else:
                reddit.subreddit("FITMostar").submit(
                    f'{postData["title"]} | {postData["author"]}',
                    selftext=html2md.convert(postData["content"])
                    + f'\n\n [Link do obavijesti.]({postData["article_url"]})',
                    flair_id="f7b632d0-cd25-11eb-9037-0e1440c58fd5",
                )
                print("Posted text")
        else:
            print("Not posting to Reddit.")


def setup(bot):
    bot.add_cog(scraper(bot))
