# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import os
from datetime import datetime as dt
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

from .connections import client_connection, redis_connection, vc_connection

LOGS = getLogger(__name__)

START_TIME = dt.now()

# remove the old logs file.
if os.path.exists("ultroid.log"):
    os.remove("ultroid.log")

# start logging into a new file.
basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=INFO,
    handlers=[FileHandler("ultroid.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)

udB = redis_connection()

ultroid_bot = client_connection()

vcbot = vc_connection(udB)

if udB.get("HNDLR"):
    HNDLR = udB.get("HNDLR")
else:
    udB.set("HNDLR", ".")
    HNDLR = udB.get("HNDLR")

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if not udB.get("SUDOS"):
    udB.set("SUDOS", "777000")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")
