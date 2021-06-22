# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from datetime import datetime

from pyUltroid.functions.asst_fns import *
from pyUltroid.misc import owner_and_sudos
from telethon import events
from telethon.utils import get_display_name

from plugins import *

from . import *

Owner_info_msg = f"""
**PEMILIK** - {OWNER_NAME}
**ID PEMILIK** - `{OWNER_ID}`

**pesan terusan** - {udB.get("PMBOT")}

__sakura {ultroid_version}, powered by @levinachannel__
"""

_settings = [
    [
        Button.inline("ᴀᴘɪ ᴋᴇʏs", data="apiset"),
        Button.inline("ᴘᴍ ʙᴏᴛ", data="chatbot"),
    ],
    [
        Button.inline("ᴀʟɪᴠᴇ", data="alvcstm"),
        Button.inline("ᴘᴍ ᴘᴇʀᴍɪᴛ", data="ppmset"),
    ],
    [Button.inline("ғᴇᴀᴛᴜʀᴇs", data="otvars")],
    [Button.inline("ᴠᴄ sᴏɴɢ ʙᴏᴛ", data="vcb")],
    [Button.inline("« ʙᴀᴄᴋ", data="mainmenu")],
]

_start = [
    [
        Button.inline("🏳️‍🌈 ʙᴀʜᴀsᴀ", data="lang"),
        Button.inline("⚙️ ᴘᴇɴɢᴀᴛᴜʀᴀɴ", data="setter"),
    ],
    [
        Button.inline("✨ sᴛᴀᴛs", data="stat"),
        Button.inline("📻 ʙʀᴏᴀᴅᴄᴀsᴛ", data="bcast"),
    ],
]


@callback("ownerinfo")
async def own(event):
    await event.edit(
        Owner_info_msg,
        buttons=[Button.inline("🗑 CLOSE", data=f"closeit")],
    )


@callback("closeit")
async def closet(lol):
    await lol.delete()


@asst_cmd("start ?(.*)")
async def ultroid(event):
    if event.is_group:
        if str(event.sender_id) in owner_and_sudos():
            return await event.reply(
                "`saya tidak bekerja didalam grup`",
                buttons=[
                    Button.url(
                        "🌸 sᴛᴀʀᴛ 🌸", url=f"https://t.me/{asst.me.username}?start=set"
                    )
                ],
            )
    else:
        if (
            not is_added(event.sender_id)
            and str(event.sender_id) not in owner_and_sudos()
        ):
            add_user(event.sender_id)
        if str(event.sender_id) not in owner_and_sudos():
            ok = ""
            u = await event.client.get_entity(event.chat_id)
            if not udB.get("STARTMSG"):
                if udB.get("PMBOT") == "True":
                    ok = "🌸 anda bisa kirim pesan ke tuan saya melalui bot ini.\n\n🌸 kirimkan pesan mu, saya akan meneruskan nya ke tuan saya."
                await event.reply(
                    f"🌸 hai [{get_display_name(u)}](tg://user?id={u.id}), ini adalah sakura asisstant bot milik [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.uid})!\n\n{ok}",
                    buttons=[Button.inline("Info.", data="ownerinfo")],
                )
            else:
                me = f"[{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.uid})"
                mention = f"[{get_display_name(u)}](tg://user?id={u.id})"
                await event.reply(
                    Redis("STARTMSG").format(me=me, mention=mention),
                    buttons=[Button.inline("Info.", data="ownerinfo")],
                )
        else:
            name = get_display_name(event.sender_id)
            if event.pattern_match.group(1) == "set":
                await event.reply(
                    "pilih pengaturan dibawah ini -",
                    buttons=_settings,
                )
            else:
                await event.reply(
                    get_string("ast_3").format(name),
                    buttons=_start,
                )


@callback("mainmenu")
@owner
async def ultroid(event):
    if event.is_group:
        return
    await event.edit(
        get_string("ast_3").format(OWNER_NAME),
        buttons=_start,
    )


@callback("stat")
@owner
async def botstat(event):
    ok = len(get_all_users())
    msg = """sakura asisstant - statistik
total pengguna - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast")
@owner
async def bdcast(event):
    ok = get_all_users()
    await event.edit(f"broadcast ke {len(ok)} pengguna.")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "kirimkan pesan untuk broadcast.\nklik /cancel untuk membatalkan broadcast.",
        )
        response = conv.wait_event(events.NewMessage(chats=OWNER_ID))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message("dibatalkan !!")
        else:
            success = 0
            fail = 0
            await conv.send_message(f"memulai broadcast ke {len(ok)} pengguna...")
            start = datetime.now()
            for i in ok:
                try:
                    await asst.send_message(int(i), f"{themssg}")
                    success += 1
                except BaseException:
                    fail += 1
            end = datetime.now()
            time_taken = (end - start).seconds
            await conv.send_message(
                f"""
broadcast selesai dalam {time_taken} detik.
total pengguna di bot - {len(ok)}
terkirim ke {success} pengguna.
gagal ke {fail} pengguna(s).""",
            )


@callback("setter")
@owner
async def setting(event):
    await event.edit(
        "pilih pengaturan dibawah ini -",
        buttons=_settings,
    )
