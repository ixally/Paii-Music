# Calls Music 1 - Telegram bot for streaming audio in group calls
# Copyright (C) 2021  Roj Serbest

from asyncio.queues import QueueEmpty
from MusicMan.config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from MusicMan.function.admins import set
from MusicMan.helpers.channelmusic import get_chat_id
from MusicMan.helpers.decorators import authorized_users_only, errors
from MusicMan.helpers.filters import command, other_filters
from MusicMan.services.callsmusic import callsmusic


@Client.on_message(filters.command(["channelpause","cpause"]) & filters.group)
@errors
@authorized_users_only
async def pause(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Apakah obrolan terhubung?**")
        return    

    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("❗ **Nothing is playing!**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text("▶️ **Paused!**")


@Client.on_message(filters.command(["channelresume","cresume"]) & filters.group)
@errors
@authorized_users_only
async def resume(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Apakah obrolan terhubung?**")
        return    

    chat_id = chid
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❗ **Tidak ada lagu yang sedang di putar**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text("⏸ **Resumed!**")


@Client.on_message(filters.command(["channelend","cend"]) & filters.group)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Apakah obrolan terhubung?**")
        return    

    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **Ga ada lagu ko nge end goblokk**")
    else:
        try:
            callsmusic.queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("❌ **lagu udh berhenti sesuai perintah bang jamet 🤡**")


@Client.on_message(filters.command(["channelskip","cskip"]) & filters.group)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    try:
        conchat = await _.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Apakah obrolan terhubung?**")
        return    

    chat_id = chid
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ **Sabar lah main skip skip bae**")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, callsmusic.queues.get(chat_id)["file"]
            )

        await message.reply_text("⏩ **lagu udh diskip sesuai perintah bang jamet 🤡**")


@Client.on_message(filters.command("channeladmincache"))
@errors
async def admincache(client, message: Message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("**Apakah obrolan terhubung?**")
        return

    set(
        chid,
        (
            member.user
            for member in await conchat.linked_chat.get_members(
                filter="administrators"
            )
        ),
    )

    await message.reply_text("✅️ **Bot** sudah **Direstart**")
