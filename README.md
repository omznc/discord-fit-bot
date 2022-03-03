# FIT Discord Bot
A custom made bot for https://discord.io/FITMostar

You probably won't be able to run this bot without changing a bunch of hardcoded variables, like channel IDs, emoji IDs and such, but I am releasing the code anyway.

I do not vouch that this repository will be updated with the production code that the bot is running right now, because I just don't have the time to do that.

## Cogs
---
Below here are all the custom modules the bot is using.

They can be easily `/cogs enable`-d and `/cogs disable`-d, among other things. You can manually disable a cog from loading by either removing it from data/cogs, or renaming it so it doesn't end on .py (I use .disabled so the `/cogs` commands work with it)

| Cog 	| Description 	|
|---	|---	|
| custom_commands 	| Handles creation, editing, removal, and display of custom slash commands. 	|
| confessions 	| Publicly, but anonymously confess something using `/confess`. 	|
| join_message 	| Sends a DM to a user that joins the server. 	|
| notify_roles 	| Notifies people that they should probably grab some `/roles`. 	|
| pins 	| Handles #pins, uses Webhooks to make it look like a user sent the pin. 	|
| role_picker 	| A custom, and very hard-coded role picker system that uses buttons. 	|
| schedule 	| Figures out what year you are (ahem, `/roles`) and sends you the schedule. 	|
| scraper 	| Scrapes new posts from fit.ba/student, then sends them to a channel using a Webhook with the professor's name and photo. 	|
| voice_channels 	| Automatically creates voice channels depending on if the current ones are used. 	|
| voice_text 	| Gives access to the voice-text channel, but only if you're in a voice channel. 	|

## So, you really want to make this work?
There are a lot of things you'd have to do to make this bot run, here are some of them:
### 1. **scraper**
- Provide `txtBrojDosijea`, `txtLozinka`, `webhook_url`, `roleTagID`, `channelID`, `guild_id`, and optionally `redditdata` in `data/config.json`.
### 2. **confessions**
- Provide `self.confessions_webhook_url`, `self.confessions_user_avatar_url`, and `self.confessions_channel_id` in `data/cogs/confessions.py`.
### 3. **notify_roles**
- Setup `self.chosen_roles` and provide a list of roles the user _should_ have, in `data/cogs/notify_roles.py`.
### 4. **pins**
- Provide `self.pins_channel_id` in `data/cogs/pins.py`, and make sure the channel has a bot-accessible webhook.
### 5. **role_picker**
- Honestly, don't even try. Sorry about the spaghetti code.
### 6. **schedule**
- Provide `self.year_roles` in `data/cogs/schedule.py`, and make sure `data/rasporedi.json` have up-to-date image links.
### 7. **voice_text**
- Provide `self.voice_text_channel_id` in `data/cogs/voice_text.py`.
### 8. **custom_commands**, **join_message**, and **voice_channels**
- These should work as-is.
### 9. **main**
- Set `TOKEN` and `GUILDID` in `main.py`

You can manually disable any cog from loading by simply adding .disabled to the end of its name.

## Contributing
No need. Please.

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html), so you can do a lot of things with it. Have fun, I guess.
