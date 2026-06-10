import os
import threading
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from ssnbot import DB_URL

# ====================== اتصال به MongoDB ======================
try:
    client = MongoClient(DB_URL, serverSelectionTimeoutMS=10000)
    # تست اتصال
    client.server_info()
    
    # استخراج نام دیتابیس از URL
    db_name = DB_URL.split('/')[-1].split('?')[0]
    if not db_name:
        db_name = "sessionbot"
    
    db = client[db_name]
    broadcast_col = db["broadcast"]
    
    print(f"✅ Successfully connected to MongoDB | Database: {db_name}")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    raise

# Lock برای جلوگیری از Race Condition (مشابه کد اصلی)
INSERTION_LOCK = threading.RLock()


# ====================== توابع ======================

async def add_user(user_id: int, user_name: str):
    """اضافه کردن یا آپدیت کاربر"""
    with INSERTION_LOCK:
        try:
            broadcast_col.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "user_name": user_name}},
                upsert=True
            )
        except PyMongoError as e:
            print(f"Error adding user {user_id}: {e}")


async def is_user(user_id: int):
    """چک کردن وجود کاربر"""
    with INSERTION_LOCK:
        try:
            user = broadcast_col.find_one({"user_id": user_id})
            return user["user_id"] if user else False
        except PyMongoError as e:
            print(f"Error checking user {user_id}: {e}")
            return False


async def query_msg():
    """گرفتن لیست همه user_id ها"""
    try:
        users = broadcast_col.find(
            {}, 
            {"user_id": 1, "_id": 0}
        ).sort("user_id", 1)
        return [user["user_id"] for user in users]
    except PyMongoError as e:
        print(f"Error querying users: {e}")
        return []


async def del_user(user_id: int):
    """حذف کاربر"""
    with INSERTION_LOCK:
        try:
            broadcast_col.delete_one({"user_id": user_id})
        except PyMongoError as e:
            print(f"Error deleting user {user_id}: {e}")
