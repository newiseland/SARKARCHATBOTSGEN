import asyncio
import logging
import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID, MONGO_URL(
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    HELP_START,
    SOURCE_READ,
)

GSTART = """**ʜᴇʏ ᴅᴇᴀʀ {}**\n\n**ᴛʜᴀɴᴋs ғᴏʀ sᴛᴀʀᴛ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ʟᴀɴɢᴜᴀɢᴇ ʙʏ ᴄʟɪᴄᴋ ᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs.**\n**ᴄʟɪᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ғᴀᴠᴏᴜʀɪᴛᴇ ʟᴀɴɢᴜᴀɢᴇ ᴛᴏ sᴇᴛ ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ ғᴏʀ ʙᴏᴛ ʀᴇᴘʟʏ.**\n\n**ᴛʜᴀɴᴋ ʏᴏᴜ ᴘʟᴇᴀsᴇ ᴇɴɪᴏʏ.**"""
STICKER = [
    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA",
    "CAACAgUAAx0CYlaJawABBy4rZaid77Tf70SV_CfjmbMgdJyVD8sAApwLAALGXCFXmCx8ZC5nlfQeBA",
    "CAACAgUAAx0CYlaJawABBy4jZaidvIXNPYnpAjNnKgzaHmh3cvoAAiwIAAIda2lVNdNI2QABHuVVHgQ",
]


EMOJIOS = [
    "💣",
    "💥",
    "🪄",
    "🧨",
    "⚡",
    "🤡",
    "👻",
    "🎃",
    "🎩",
    "🕊",
]

BOT = "https://envs.sh/IL_.jpg"
IMG = [
    "https://graph.org/file/210751796ff48991b86a3.jpg",
    "https://graph.org/file/7b4924be4179f70abcf33.jpg",
    "https://graph.org/file/f6d8e64246bddc26b4f66.jpg",
    "https://graph.org/file/63d3ec1ca2c965d6ef210.jpg",
    "https://graph.org/file/9f12dc2a668d40875deb5.jpg",
    "https://graph.org/file/0f89cd8d55fd9bb5130e1.jpg",
    "https://graph.org/file/e5eb7673737ada9679b47.jpg",
    "https://graph.org/file/2e4dfe1fa5185c7ff1bfd.jpg",
    "https://graph.org/file/36af423228372b8899f20.jpg",
    "https://graph.org/file/c698fa9b221772c2a4f3a.jpg",
    "https://graph.org/file/61b08f41855afd9bed0ab.jpg",
    "https://graph.org/file/744b1a83aac76cb3779eb.jpg",
    "https://graph.org/file/814cd9a25dd78480d0ce1.jpg",
    "https://graph.org/file/e8b472bcfa6680f6c6a5d.jpg",
]

# Initialize MongoDB
mongo = MongoClient(MONGO_URL)
db = mongo["ChatBotStatusDb"]
chats_collection = db["Chats"]
users_collection = db["Users"]

# Bot client
nexichat = Client("nexichat")

# Sticker & Image Lists
STICKERS = [
    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA",
    "CAACAgUAAx0CYlaJawABBy4rZaid77Tf70SV_CfjmbMgdJyVD8sAApwLAALGXCFXmCx8ZC5nlfQeBA",
]

IMG_LIST = [
    "https://graph.org/file/1ac13effa55a82dc9b881-2bf2ae8fd65ca218ac.jpg",
    "https://graph.org/file/9f12dc2a668d40875deb5.jpg",
    "https://graph.org/file/c698fa9b221772c2a4f3a.jpg",
]

# Broadcast lock and flag
broadcast_lock = asyncio.Lock()
IS_BROADCASTING = False

# MongoDB helper functions
async def get_served_chats():
    return list(chats_collection.find())

async def add_served_chat(chat_id):
    if not chats_collection.find_one({"chat_id": chat_id}):
        chats_collection.insert_one({"chat_id": chat_id})

async def get_served_users():
    return list(users_collection.find())

async def add_served_user(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})

# Start command
@nexichat.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
        sticker = await message.reply_sticker(random.choice(STICKERS))
        await asyncio.sleep(1.5)
        await sticker.delete()
        await message.reply_photo(
            photo=random.choice(IMG_LIST),
            caption="**Hey! I'm alive and ready to chat!**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Help", callback_data="help")],
                [InlineKeyboardButton("Repo", url="https://github.com/your-repo")],
            ])
        )
    else:
        await add_served_chat(message.chat.id)
        await message.reply_photo(
            photo=random.choice(IMG_LIST),
            caption="Thanks for adding me to the group!"
        )

# Stats command
@nexichat.on_message(filters.command("stats"))
async def stats_cmd(client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_photo(
        photo=random.choice(IMG_LIST),
        caption=f"**Bot Stats:**\n\n• Users: {users}\n• Chats: {chats}"
    )

# Broadcast command
@nexichat.on_message(filters.command(["broadcast", "gcast"]) & filters.user(int(OWNER_ID)))
async def broadcast_message(client, message: Message):
    global IS_BROADCASTING
    async with broadcast_lock:
        if IS_BROADCASTING:
            return await message.reply_text("A broadcast is already in progress. Please wait.")
        
        IS_BROADCASTING = True
        try:
            query = message.text.split(None, 1)[1].strip()
        except IndexError:
            return await message.reply_text("Give some message to broadcast!")

        flags = {
            "-pin": "-pin" in query,
            "-pinloud": "-pinloud" in query,
            "-nogroup": "-nogroup" in query,
            "-user": "-user" in query,
        }

        for flag in flags:
            query = query.replace(flag, "").strip()

        broadcast_type = "reply" if message.reply_to_message else "text"
        broadcast_content = message.reply_to_message if message.reply_to_message else query

        await message.reply_text("**Started broadcasting...**")

        if not flags["-nogroup"]:
            sent = 0
            pin_count = 0
            chats = await get_served_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                try:
                    if broadcast_type == "reply":
                        m = await client.forward_messages(chat_id, message.chat.id, [broadcast_content.id])
                    else:
                        m = await client.send_message(chat_id, broadcast_content)
                    sent += 1

                    if flags["-pin"] or flags["-pinloud"]:
                        try:
                            await m.pin(disable_notification=flags["-pin"])
                            pin_count += 1
                        except Exception:
                            continue

                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    logging.error(f"Broadcast error in chat {chat_id}: {e}")
                    continue

            await message.reply_text(f"**Broadcasted to {sent} chats, pinned in {pin_count} chats.**")

        if flags["-user"]:
            susr = 0
            users = await get_served_users()
            for user in users:
                user_id = int(user["user_id"])
                try:
                    if broadcast_type == "reply":
                        await client.forward_messages(user_id, message.chat.id, [broadcast_content.id])
                    else:
                        await client.send_message(user_id, broadcast_content)
                    susr += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as e:
                    logging.error(f"Broadcast error for user {user_id}: {e}")
                    continue

            await message.reply_text(f"**Broadcasted to {susr} users.**")

        IS_BROADCASTING = False

# Start the bot
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Bot started.")
    nexichat.run()
