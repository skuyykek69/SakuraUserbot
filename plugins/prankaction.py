# sakura userbot
# prank promote and demote plugin

"""
📚 Commands Available -
• `{i}fpromote`

• `{i}npromote`

• `{i}fdemote`

• `{i}ndemote`

📝 __aksi prank promote dan demote, lakukan aksi prank promote & demote ke teman di dalam grup.__
"""

import random, re
from uniborg.util import admin_cmd
import asyncio
from telethon import events

@borg.on(admin_cmd(pattern="fpromote ?(.*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("`SYSTEM`:**mempromosikan pengguna..**")
        await asyncio.sleep(1)
        await event.edit("`SYSTEM`:**mempromosikan pengguna...**")
        await asyncio.sleep(1)
        await event.edit("`SYSTEM`:**mempromosikan pengguna....**")
        await asyncio.sleep(1)
        await event.edit("`SYSTEM`:**BERHASIL MEMPROMOSIKAN PENGGUNA**")
        
        
@borg.on(admin_cmd(pattern="npromote ?(.*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("`SYSTEM`:**mempromosikan pengguna..**")
        await asyncio.sleep(1)
        await event.edit("`SYSTEM`:**mempromosikan pengguna...**")
        await asyncio.sleep(1)
        await event.edit("`SYSTEM`:**mempromosikan pengguna....**")
        await asyncio.sleep(1)
        await event.edit("`SYSTEM`:`tidak punya izin untuk mempromosikan pengguna ini`")
        
        
        
@borg.on(admin_cmd(pattern="ndemote ?(.*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("`😈Userbot😈`:**DEMOTING USER..**")
        await asyncio.sleep(1)
        await event.edit("`😈Userbot😈`:**DEMOTING USER...**")
        await asyncio.sleep(1)
        await event.edit("`😈Userbot😈`:**DEMOTING USER....**")
        await asyncio.sleep(1)
        await event.edit("`😈Userbot😈`:**Not Enough Rights To Demote user **")
        
        
@borg.on(admin_cmd(pattern="fdemote ?(.*)"))
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit("`😈Userbot😈`:**DEMOTING USER..**")
        await asyncio.sleep(1)
        await event.edit("`😈Userbot😈`:**DEMOTING USER...**")
        await asyncio.sleep(1)
        await event.edit("`😈Userbot😈`:**DEMOTING USER....**")
        await asyncio.sleep(1)
        await event.edit("`😈Userbot😈`:**DEMOTED USER SUCCESSFULLY**")
