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
nexichat = Client("nexichat")

@nexichat.on_cmd(["start", "start"])
async def start(_, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        accha = await m.reply_text(
            text=random.choice(EMOJIOS),
        )
        await asyncio.sleep(1.3)
        await accha.edit("__𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐁𝐚𝐛𝐲 ꨄ︎ 𝐖𝐚𝐢𝐭..🥵__")
        await asyncio.sleep(0.2)
        await accha.edit("__𝐇𝐞𝐲 𝐁𝐚𝐛𝐲 ꨄ 𝐇𝐨𝐰 𝐀𝐫𝐞 𝐘𝐨𝐮⚡.....__")
        await asyncio.sleep(0.2)
        await accha.edit("__𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 ꨄ︎ 𝐁𝐚𝐛𝐲📍..__")
        await asyncio.sleep(0.2)
        await accha.delete()
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        await asyncio.sleep(2)
        await umm.delete()
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=f"""**:╭───────────────────⦿
│❖ 𝖧ᴇʏ ɪ'ᴍ ᴄʜᴀᴛʙᴏᴛ  ✨
├───────────────────⦿
│✦ ɪ ʜᴀᴠᴇ ᴍᴀɢɪᴄ ғᴇᴀᴛᴜʀᴇs.
│❍ 𝖠ᴅᴠᴀɴᴄᴇᴅ ᴀɪ ʙᴀsᴇᴅ ᴄʜᴀᴛʙᴏᴛ.
├───────────────────⦿
│✦ ɪ'ᴍ ꜱᴍᴀʀᴛ & ᴀʙᴜꜱᴇʟᴇꜱꜱ ᴄʜᴀᴛʙᴏᴛ.
│❍ ɪ ᴄᴀɴ ʜᴇʟᴘ ᴀᴄᴛɪᴠᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ.
│✦ ᴍᴜʟᴛɪ-ʟᴀɴɢ ꜱᴜᴘᴘᴏʀᴛ ʙʏ /lang.
│❍ 𝖢ʟɪᴄᴋ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ʜᴇʟᴘs.
│✦ I ᴄᴀɴ ᴛᴇʟʟ ʏᴏᴜ ᴛɪᴍᴇ ɪꜰ ʏᴏᴜ ᴀꜱᴋ.
├───────────────────⦿
│❍ Aᴄᴛɪᴠᴇ ᴜꜱᴇʀꜱ : 40000 🎉
│❖ ϻᴀᴅᴇ ʙʏ [𝐒𝐀𝐑𝐊𝐀𝐑 ✯ 𝐎𝐏](https://t.me/ll_SARKAR_OWNER_ll) 💞
╰───────────────────⦿) """,
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
        await add_served_user(m.from_user.id)
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=START,
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)
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
