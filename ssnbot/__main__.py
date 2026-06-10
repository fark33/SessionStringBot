import asyncio
import uvloop
import logging

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from pyropatch import pyropatch
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer
from ssnbot import APP_ID, API_HASH, BOT_TOKEN, LOGGER

async def main():
    plugins = dict(root="ssnbot/plugins")
    
    app = Client(
        name="ssnbot",
        api_id=APP_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins,
        sleep_threshold=60,
        workers=10,
    )
    
    async with app:
        me = await app.get_me()
        LOGGER.info(f"✅ Bot Started Successfully: {me.first_name} (@{me.username})")
        LOGGER.info(f"Pyrogram v{__version__} | Layer {layer}")
        await idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        LOGGER.error(f"❌ Critical Error: {e}", exc_info=True)
