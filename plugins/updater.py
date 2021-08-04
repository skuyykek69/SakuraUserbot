# sakura userbot
# copyright 2021 (c) by veez project
# levina-lab

"""
📚 Commands Available -
• `{i}update`
   perintah untuk memeriksa pembaruan userbot dan memperbarui nya ke versi terbaru.
"""

from git import Repo
from telethon.tl.functions.channels import ExportMessageLinkRequest as GetLink

from . import *

ULTPIC = "resources/extras/inline.jpg"
CL = udB.get("INLINE_PIC")
if CL:
    ULTPIC = CL


@ultroid_cmd(pattern="update$")
async def _(e):
    xx = await eor(e, "`memeriksa pembaruan...`")
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await ultroid_bot.asst.send_file(
            int(udB.get("LOG_CHANNEL")),
            ULTPIC,
            caption="• **UPDATE TERSEDIA** •",
            force_document=False,
            buttons=Button.inline("CHANGE LOGS", data="changes"),
        )
        Link = (await ultroid_bot(GetLink(x.chat_id, x.id))).link
        await xx.edit(
            f'<strong><a href="{Link}">[changelogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>sakura userbot anda </code><strong>sudah versi terbaru</strong><code> dengan </code><strong><a href="https://github.com/levina-lab/SakuraUserbot/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail")
@owner
async def updava(event):
    await event.delete()
    await ultroid_bot.asst.send_file(
        int(udB.get("LOG_CHANNEL")),
        ULTPIC,
        caption="✨ **PEMBARUAN TERSEDIA** ✨",
        force_document=False,
        buttons=Button.inline("CHANGE LOGS", data="changes"),
    )
