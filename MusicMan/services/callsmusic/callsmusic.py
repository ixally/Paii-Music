# Calls Music Modernized - Telegram bot for streaming audio in group calls
# Compatible with Pyrogram v2 & PyTgCalls v3
# Original credits: Roj Serbest

import asyncio
from pyrogram import Client
from pytgcalls import GroupCallFactory

from MusicMan.config import API_HASH, API_ID, SESSION_NAME
from MusicMan.services.callsmusic import queues

# --- Setup Pyrogram client ---
client = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_NAME
)
# --- Setup group call factory ---
call_factory = GroupCallFactory(client)
pytgcalls = call_factory.get_group_call()

# --- Event handler for stream end ---
@pytgcalls.on_network_status_changed
async def on_stream_end(call, is_connected):
    if not is_connected:
        return
    chat_id = call.chat_id
    queues.task_done(chat_id)

    if queues.is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        next_item = queues.get(chat_id)
        await pytgcalls.change_stream(chat_id, next_item["file"])

# --- Runner ---
# --- Runner ---
async def run():
    await client.start()

    # Pastikan userbot udah join ke grup target
    chat = await client.get_chat(-1002646031980)  # ganti ID grup lo

    # Start panggilan grup di chat itu
    await pytgcalls.start(chat.id)

    print(f"✅ PyTgCalls connected to group: {chat.title}")
    await idle()

# --- Helper for asyncio ---
async def idle():
    while True:
        await asyncio.sleep(1)
