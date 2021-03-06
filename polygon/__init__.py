# This file is distributed as a part of the polygon project (justaprudev.github.io/polygon)
# By justaprudev

from telethon.sessions import StringSession
from .polygon import Polygon
from pathlib import Path
import logging
import secrets

logging.basicConfig(level=logging.INFO)
session = secrets.SESSION

if session:
    logging.info("Polygon is now online!")
    polygon = Polygon(
        StringSession(str(session)),
        api_id=secrets.APP_ID,
        api_hash=secrets.API_HASH
    )
    polygon.run_until_disconnected()
else:
    logging.info("Please set your session string to SESSION secret.")