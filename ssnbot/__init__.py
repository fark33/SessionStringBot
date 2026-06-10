import os
import re
import logging
import logging.config
from dotenv import load_dotenv

# لود کردن متغیرهای محیط
load_dotenv(override=True)

pattern = re.compile(r"^.\d+$")

# ====================== متغیرهای اصلی ======================
APP_ID = os.environ.get("APP_ID", "")
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DB_URL = os.environ.get("DB_URL", "")
OWNER_ID = int(os.environ.get('OWNER_ID', 0))
MUST_JOIN = os.environ.get("MUST_JOIN", "")

ADMINS = [
    int(user) if pattern.search(user) else user
    for user in os.environ.get("ADMINS", "").split()
] + [OWNER_ID]

# ====================== چک کردن DB_URL برای MongoDB ======================
if DB_URL and not DB_URL.startswith("mongodb"):
    raise ValueError(
        "❌ DB_URL must be a MongoDB connection string!\n"
        "Example: mongodb+srv://user:pass@cluster0.mongodb.net/dbname"
    )
elif not DB_URL:
    raise ValueError("❌ DB_URL environment variable is not set!")

# ====================== تنظیمات Logging ======================
logging.config.fileConfig(fname='config.ini', disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pymongo").setLevel(logging.WARNING)

LOGGER.info("✅ Environment variables loaded successfully")
LOGGER.info(f"📊 Admins: {len(ADMINS)} | Owner: {OWNER_ID}")
