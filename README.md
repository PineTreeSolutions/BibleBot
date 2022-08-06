# BibleBot
Telegram bot used for calling Bible verses in chats.

After adding the bot to your chat, you can call it using the ```/bible book chapter:verse-verse``` format. Bible translation is the Authorized King James Version (with the deuterocanonical books). There are inherent limitations within Telegram on message length (4096 characters) which prevents longer selections from being displayed, so don't expect to be able to call entire chapters or books within a chat. This bot isn't meant to be a replacement for a full Bible app, but simply a tool to display small sections of the Scriptures.

Bot is deployed via Docker container. The following environment variables need to be set in order to run the bot:
`TG_WEBHOOK_URL` - URL for the Telegram webhook
`TG_TOKEN` - your bot's secret token
`PORT` - Port you want the Gunicorn server to run on in the Docker container, defaults to 8080 if not specified
