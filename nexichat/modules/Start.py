import asyncio
import logging
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from config import OWNER_ID, MONGO_URL

# Initialize MongoDB
mongo = MongoClient(MONGO_URL)
db = mongo["ChatBotStatusDb"]
chats_collection = db["Chats"]
users_collection = db["Users"]

# Bot client

# Broadcast lock and flag
broadcast_lock = asyncio.Lock()
IS_BROADCASTING = False

# Helper functions
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

# Stats command
@nexichat.on_message(filters.command("stats"))
async def stats(client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_text(f"**Stats:**\nChats: {chats}\nUsers: {users}")

# Start bot
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Bot started.")
    nexichat.run()
