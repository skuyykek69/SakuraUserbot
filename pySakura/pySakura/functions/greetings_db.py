# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from .. import udB

try:
    eval(udB.get("WELCOME"))
except BaseException:
    udB.set("WELCOME", "{}")

try:
    eval(udB.get("GOODBYE"))
except BaseException:
    udB.set("GOODBYE", "{}")


def add_welcome(chat, msg, media):
    ok = eval(udB.get("WELCOME"))
    ok.update({chat: {"welcome": msg, "media": media}})
    return udB.set("WELCOME", str(ok))


def get_welcome(chat):
    ok = eval(udB.get("WELCOME"))
    wl = ok.get(chat)
    if wl:
        return wl
    return


def delete_welcome(chat):
    ok = eval(udB.get("WELCOME"))
    wl = ok.get(chat)
    if wl:
        ok.pop(chat)
        return udB.set("WELCOME", str(ok))
    return


def add_goodbye(chat, msg, media):
    ok = eval(udB.get("GOODBYE"))
    ok.update({chat: {"goodbye": msg, "media": media}})
    return udB.set("GOODBYE", str(ok))


def get_goodbye(chat):
    ok = eval(udB.get("GOODBYE"))
    wl = ok.get(chat)
    if wl:
        return wl
    return


def delete_goodbye(chat):
    ok = eval(udB.get("GOODBYE"))
    wl = ok.get(chat)
    if wl:
        ok.pop(chat)
        return udB.set("GOODBYE", str(ok))
    return
