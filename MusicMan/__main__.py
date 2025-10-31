import asyncio
import requests
from pyrogram import Client as Bot

from MusicMan.config import API_HASH, API_ID, BG_IMAGE, BOT_TOKEN
from MusicMan.services.callsmusic.callsmusic import pytgcalls
# Download background image
response = requests.get(BG_IMAGE)
with open("./etc/foreground.png", "wb") as file:
    file.write(response.content)

bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="MusicMan.modules"),
)


async def main():
    await bot.start()
    print("bot music sudah aktif")
    await idle()
    await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
