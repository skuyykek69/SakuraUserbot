# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import asyncio
import os
import time
import traceback
import urllib
from pathlib import Path
from random import randint
from urllib.request import urlretrieve

import telethon.utils
from pytz import timezone
from telethon import TelegramClient
from telethon import __version__ as vers
from telethon.errors.rpcerrorlist import (
    AccessTokenExpiredError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
    ChannelsTooMuchError,
    PhoneNumberInvalidError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)

from . import *
from .dB import DEVLIST
from .dB.database import Var
from .functions.all import updater
from .utils import load_addons, load_assistant, load_plugins, load_pmbot
from .version import __version__ as ver

x = ["resources/auths", "resources/downloads", "addons"]
for x in x:
    if not os.path.isdir(x):
        os.mkdir(x)

if udB.get("CUSTOM_THUMBNAIL"):
    urlretrieve(udB.get("CUSTOM_THUMBNAIL"), "resources/extras/ultroid.jpg")

if udB.get("GDRIVE_TOKEN"):
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(udB.get("GDRIVE_TOKEN"))

if udB.get("MEGA_MAIL") and udB.get("MEGA_PASS"):
    with open(".megarc", "w") as mega:
        mega.write(
            f'[Login]\nUsername = {udB.get("MEGA_MAIL")}\nPassword = {udB.get("MEGA_PASS")}'
        )

if udB.get("TIMEZONE"):
    try:
        timezone(udB.get("TIMEZONE"))
        os.environ["TZ"] = timezone(udB.get("TIMEZONE"))
        time.tzset()
    except BaseException:
        LOGS.info(
            "Incorrect Timezone ,\nCheck Available Timezone From Here https://telegra.ph/Ultroid-06-18-2\nSo Time is Default UTC"
        )
        os.environ["TZ"] = "UTC"
        time.tzset()


async def autobot():
    await ultroid_bot.start()
    if Var.BOT_TOKEN:
        udB.set("BOT_TOKEN", str(Var.BOT_TOKEN))
        return
    if udB.get("BOT_TOKEN"):
        return
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather , Please Kindly Wait")
    who = await ultroid_bot.get_me()
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "ultroid_" + (str(who.id))[5:] + "_bot"
    bf = "Botfather"
    await ultroid_bot(UnblockRequest(bf))
    await ultroid_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await ultroid_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        LOGS.info(
            "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
        )
        exit(1)
    await ultroid_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await ultroid_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.info(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            exit(1)
    await ultroid_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
    await ultroid_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "ultroid_" + (str(who.id))[6:] + str(ran) + "_bot"
        await ultroid_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await ultroid_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            udB.set("BOT_TOKEN", token)
            await ultroid_bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(bf, "Search")
            LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
        else:
            LOGS.info(
                f"Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )
            exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        udB.set("BOT_TOKEN", token)
        await ultroid_bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await ultroid_bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await ultroid_bot.send_message(bf, "Search")
        LOGS.info(f"DONE YOUR TELEGRAM BOT IS CREATED SUCCESSFULLY @{username}")
    else:
        LOGS.info(
            f"Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )
        exit(1)


if not udB.get("BOT_TOKEN"):
    ultroid_bot.loop.run_until_complete(autobot())


async def istart(ult):
    await ultroid_bot.start(ult)
    ultroid_bot.me = await ultroid_bot.get_me()
    ultroid_bot.uid = telethon.utils.get_peer_id(ultroid_bot.me)
    ultroid_bot.first_name = ultroid_bot.me.first_name
    if not ultroid_bot.me.bot:
        udB.set("OWNER_ID", ultroid_bot.uid)


async def autopilot():
    await ultroid_bot.start()
    if Var.LOG_CHANNEL and str(Var.LOG_CHANNEL).startswith("-100"):
        udB.set("LOG_CHANNEL", str(Var.LOG_CHANNEL))
    k = []  # To Refresh private ids
    async for x in ultroid_bot.iter_dialogs():
        k.append(x.id)
    if udB.get("LOG_CHANNEL"):
        try:
            await ultroid_bot.get_entity(int(udB.get("LOG_CHANNEL")))
            return
        except BaseException:
            udB.delete("LOG_CHANNEL")
    try:
        r = await ultroid_bot(
            CreateChannelRequest(
                title="My Ultroid Logs",
                about="My Ultroid Log Group\n\n Join @TeamUltroid",
                megagroup=True,
            ),
        )
    except ChannelsTooMuchError:
        LOGS.info(
            "You Are On Too Many Channels & Groups , Leave some And Restart The Bot"
        )
        exit(1)
    except BaseException:
        LOGS.info(
            "Something Went Wrong , Create A Group and set its id on config var LOG_CHANNEL."
        )
        exit(1)
    chat_id = r.chats[0].id
    if not str(chat_id).startswith("-100"):
        udB.set("LOG_CHANNEL", "-100" + str(chat_id))
    else:
        udB.set("LOG_CHANNEL", str(chat_id))
    rights = ChatAdminRights(
        add_admins=True,
        invite_users=True,
        change_info=True,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        anonymous=False,
        manage_call=True,
    )
    await ultroid_bot(EditAdminRequest(chat_id, asst.me.username, rights, "Assistant"))
    pfpa = await ultroid_bot.download_profile_photo(chat_id)
    if not pfpa:
        urllib.request.urlretrieve(
            "https://telegra.ph/file/bac3a1c21912a7b35c797.jpg", "channelphoto.jpg"
        )
        ll = await ultroid_bot.upload_file("channelphoto.jpg")
        await ultroid_bot(EditPhotoRequest(chat_id, InputChatUploadedPhoto(ll)))
        os.remove("channelphoto.jpg")
    else:
        os.remove(pfpa)


ultroid_bot.asst = None


async def bot_info(asst):
    await asst.start()
    asst.me = await asst.get_me()
    return asst.me


LOGS.info("Initialising...")
LOGS.info(f"py-Ultroid Version - {ver}")
LOGS.info(f"Telethon Version - {vers}")
LOGS.info("Ultroid Version - 0.0.8.1")


# log in
BOT_TOKEN = udB.get("BOT_TOKEN")
LOGS.info("Starting Ultroid...")
try:
    ultroid_bot.asst = TelegramClient(
        "asst-session", api_id=Var.API_ID, api_hash=Var.API_HASH
    ).start(bot_token=BOT_TOKEN)
    asst = ultroid_bot.asst
    ultroid_bot.loop.run_until_complete(istart(asst))
    ultroid_bot.loop.run_until_complete(bot_info(asst))
    LOGS.info("Done, startup completed")
    LOGS.info("UserBot - Started")
except AuthKeyDuplicatedError or PhoneNumberInvalidError or EOFError:
    LOGS.info("Session String expired. Please create a new one! Ultroid is stopping...")
    exit(1)
except ApiIdInvalidError:
    LOGS.info("Your API ID/API HASH combination is invalid. Kindly recheck.")
    exit(1)
except AccessTokenExpiredError:
    udB.delete("BOT_TOKEN")
    LOGS.info(
        "BOT_TOKEN expired , So Quitted The Process, Restart Again To create A new Bot. Or Set BOT_TOKEN env In Vars"
    )
    exit(1)
except BaseException:
    LOGS.info("Error: " + str(traceback.print_exc()))
    exit(1)


if str(ultroid_bot.uid) not in DEVLIST:
    chat = eval(udB.get("BLACKLIST_CHATS"))
    if -1001327032795 not in chat:
        chat.append(-1001327032795)
        udB.set("BLACKLIST_CHATS", str(chat))

ultroid_bot.loop.run_until_complete(autopilot())

# for userbot
files = sorted(os.listdir("plugins"))
for plugin_name in files:
    try:
        if plugin_name.endswith(".py"):
            load_plugins(plugin_name[:-3])
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"Ultroid - Official -  Installed - {plugin_name}")
    except Exception:
        LOGS.info(f"Ultroid - Official - ERROR - {plugin_name}")
        LOGS.info(str(traceback.print_exc()))


# for assistant
files = sorted(os.listdir("assistant"))
for plugin_name in files:
    try:
        if plugin_name.endswith(".py"):
            load_assistant(plugin_name[:-3])
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"Ultroid - Assistant -  Installed - {plugin_name}")
    except Exception:
        LOGS.info(f"Ultroid - Assistant - ERROR - {plugin_name}")
        LOGS.info(str(traceback.print_exc()))

# for addons
addons = udB.get("ADDONS")
if addons == "True" or addons is None:
    try:
        os.system("git clone https://github.com/TeamUltroid/UltroidAddons.git addons/")
    except BaseException:
        pass
    LOGS.info("Installing packages for addons")
    os.system("pip install -r addons/addons.txt")
    files = sorted(os.listdir("addons"))
    for plugin_name in files:
        try:
            if plugin_name.endswith(".py"):
                load_addons(plugin_name[:-3])
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.info(f"Ultroid - Addons -  Installed - {plugin_name}")
        except Exception:
            LOGS.info(f"Ultroid - Addons - ERROR - {plugin_name}")
            LOGS.info(str(traceback.print_exc()))
else:
    os.system("cp plugins/__init__.py addons/")

# for channel plugin
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:

    async def plug():
        try:
            if Plug_channel.startswith("@"):
                chat = Plug_channel
            else:
                try:
                    chat = int(Plug_channel)
                except BaseException:
                    return
            async for x in ultroid_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument
            ):
                await asyncio.sleep(0.6)
                files = await ultroid_bot.download_media(x.media, "./addons/")
                file = Path(files)
                plugin = file.stem
                if "(" not in files:
                    try:
                        load_addons(plugin.replace(".py", ""))
                        LOGS.info(f"Ultroid - PLUGIN_CHANNEL - Installed - {plugin}")
                    except Exception as e:
                        LOGS.info(f"Ultroid - PLUGIN_CHANNEL - ERROR - {plugin}")
                        LOGS.info(str(e))
                else:
                    LOGS.info(f"Plugin {plugin} is Pre Installed")
                    os.remove(files)
        except Exception as e:
            LOGS.info(str(e))


# chat via assistant
pmbot = udB.get("PMBOT")
if pmbot == "True":
    files = sorted(os.listdir("assistant/pmbot"))
    for plugin_name in files:
        if plugin_name.endswith(".py"):
            load_pmbot(plugin_name[:-3])
    LOGS.info(f"Ultroid - PM Bot Message Forwards - Enabled.")

# customize assistant


async def customize():
    try:
        chat_id = int(udB.get("LOG_CHANNEL"))
        xx = await ultroid_bot.get_entity(asst.me.username)
        if xx.photo is None:
            LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
            UL = f"@{asst.me.username}"
            if (ultroid_bot.me.username) is None:
                sir = ultroid_bot.me.first_name
            else:
                sir = f"@{ultroid_bot.me.username}"
            await ultroid_bot.send_message(
                chat_id, "Auto Customisation Started on @botfather"
            )
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/cancel")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/setuserpic")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_file(
                "botfather", "resources/extras/ultroid_assistant.jpg"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setabouttext")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setdescription")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather",
                f"✨ PowerFul Ultroid Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @TeamUltroid ✨",
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message(
                chat_id, "**Auto Customisation** Done at @BotFather"
            )
            LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.warning(str(e))


# some stuffs
async def ready():
    chat_id = int(udB.get("LOG_CHANNEL"))
    MSG = f"**Ultroid has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖\n**Support**: @TeamUltroid\n➖➖➖➖➖➖➖➖➖"
    BTTS = [Button.inline("Help", "open")]
    updava = await updater()
    try:
        if updava:
            BTTS = [
                [Button.inline("Update Available", "updtavail")],
                [Button.inline("Help", "open")],
            ]
        await ultroid_bot.asst.send_message(chat_id, MSG, buttons=BTTS)
    except BaseException:
        try:
            await ultroid_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    try:
        # To Let Them know About New Updates and Changes
        await ultroid_bot(JoinChannelRequest("@TheUltroid"))
    except BaseException:
        pass


ws = f"WEBSOCKET_URL=http://localhost:6969"
lg = f"LOG_CHANNEL={udB.get('LOG_CHANNEL')}"
bt = f"BOT_TOKEN={udB.get('BOT_TOKEN')}"
try:
    with open(".env", "r") as x:
        m = x.read()
    if "WEBSOCKET_URL" not in m:
        with open(".env", "a+") as t:
            t.write("\n" + ws)
    if "LOG_CHANNEL" not in m:
        with open(".env", "a+") as t:
            t.write("\n" + lg)
    if "BOT_TOKEN" not in m:
        with open(".env", "a+") as t:
            t.write("\n" + bt)
except BaseException:
    with open(".env", "w") as t:
        t.write(ws + "\n" + lg + "\n" + bt)


ultroid_bot.loop.run_until_complete(customize())
if Plug_channel:
    ultroid_bot.loop.run_until_complete(plug())
ultroid_bot.loop.run_until_complete(ready())

LOGS.info(
    """
                ----------------------------------------------------------------------
                    Ultroid has been deployed! Visit @TheUltroid for updates!!
                ----------------------------------------------------------------------
"""
)


ultroid_bot.run_until_disconnected()
