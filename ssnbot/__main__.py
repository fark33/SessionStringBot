import asyncio
import uvloop
import logging

# تنظیم uvloop قبل از هر چیز
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from pyropatch import pyropatch  # noqa: E402, F401
from pyrogram import Client, idle, __version__  # noqa: E402
from pyrogram.raw.all import layer  # noqa: E402
from ssnbot import APP_ID, API_HASH, BOT_TOKEN, LOGGER  # noqa: E402

# رفع DeprecationWarning مربوط به event loop
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

async def main():
    plugins = dict(root="ssnbot/plugins")
    
    app = Client(
        name="ssnbot",
        api_id=APP_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins,
        # تنظیمات اضافی برای پایداری
        sleep_threshold=60,
        workers=10,
    )
    
    async with app:
        me = await app.get_me()
        LOGGER.info(
            "%s - @%s - Pyrogram v%s (Layer %s) - Started Successfully ✅",
            me.first_name,
            me.username,
            __version__,
            layer,
        )
        await idle()
        LOGGER.info("%s - @%s - Stopped !!!", me.first_name, me.username)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(f"Critical error: {e}", exc_info=True)
