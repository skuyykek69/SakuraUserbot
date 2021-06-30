# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import inspect
import re
import sys
from pathlib import Path
from time import gmtime, sleep, strftime
from traceback import format_exc

from plugins import ultroid_version as ult_ver
from telethon import __version__ as telever
from telethon import events
from telethon.errors.rpcerrorlist import ChatSendInlineForbiddenError, FloodWaitError
from telethon.utils import get_display_name

from .. import HNDLR, LOGS, udB, ultroid_bot
from ..dB.core import LIST, LOADED
from ..functions.all import bash
from ..functions.all import time_formatter as tf
from ..version import __version__ as pyver
from . import should_allow_sudo, sudoers, ultroid_bot
from ._wrappers import eod

hndlr = "\\" + HNDLR

black_list_chats = eval(udB.get("BLACKLIST_CHATS"))

# decorator


def ultroid_cmd(allow_sudo=should_allow_sudo(), **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern = args["pattern"]
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)

    if pattern is not None:
        if pattern.startswith(r"\#"):
            args["pattern"] = re.compile(pattern)
        else:
            args["pattern"] = re.compile(hndlr + pattern)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                LIST[file_test].append(cmd)
            except BaseException:
                LIST.update({file_test: [cmd]})
        except BaseException:
            pass
    args["blacklist_chats"] = True
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    if "admins_only" in args:
        del args["admins_only"]
    if "groups_only" in args:
        del args["groups_only"]

    def decorator(func):
        async def wrapper(ult):
            if not allow_sudo:
                if not ult.out:
                    return
            if not ult.out and (str(ult.sender_id) not in sudoers()):
                return
            chat = await ult.get_chat()
            naam = get_display_name(chat)
            if ult.fwd_from:
                return
            if groups_only and ult.is_private:
                return await eod(ult, "`Use this in group/channel.`")
            if admins_only and not chat.admin_rights:
                return await eod(ult, "`I am not an admin.`")
            try:
                await func(ult)
            except FloodWaitError as fwerr:
                await ultroid_bot.asst.send_message(
                    int(udB.get("LOG_CHANNEL")),
                    f"`FloodWaitError:\n{str(fwerr)}\n\nSleeping for {tf((fwerr.seconds + 10)*1000)}`",
                )
                sleep(fwerr.seconds + 10)
                await ultroid_bot.asst.send_message(
                    int(udB.get("LOG_CHANNEL")),
                    "`Bot is working again`",
                )
            except ChatSendInlineForbiddenError:
                return await eod(ult, "`Inline Locked In This Chat.`")
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                LOGS.exception(e)
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                ftext = (
                    "**Ultroid Client Error:** `Forward this to` @UltroidSupport\n\n"
                )
                ftext += "`Py-Ultroid Version: " + str(pyver)
                ftext += "\nUltroid Version: " + str(ult_ver)
                ftext += "\nTelethon Version: " + str(telever) + "\n\n"
                ftext += "--------START ULTROID CRASH LOG--------"
                ftext += "\nDate: " + date
                ftext += "\nGroup: " + str(ult.chat_id) + " " + str(naam)
                ftext += "\nSender ID: " + str(ult.sender_id)
                ftext += "\nReplied: " + str(ult.is_reply)
                ftext += "\n\nEvent Trigger:\n"
                ftext += str(ult.text)
                ftext += "\n\nTraceback info:\n"
                ftext += str(format_exc())
                ftext += "\n\nError text:\n"
                ftext += str(sys.exc_info()[1])
                ftext += "\n\n--------END ULTROID CRASH LOG--------"
                ftext += "\n\n\nLast 5 commits:\n"

                stdout, stderr = await bash('git log --pretty=format:"%an: %s" -5')
                result = str(stdout.strip()) + str(stderr.strip())

                ftext += result + "`"

                await ultroid_bot.asst.send_message(
                    int(udB["LOG_CHANNEL"]),
                    ftext,
                )

        ultroid_bot.add_event_handler(wrapper, events.NewMessage(**args))
        try:
            LOADED[file_test].append(wrapper)
        except Exception:
            LOADED.update({file_test: [wrapper]})
        return wrapper

    return decorator
