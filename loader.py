import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pyrogram import Client
import nest_asyncio
import structlog
import tgcrypto

nest_asyncio.apply()

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
PUNYA_CHANNEL_ID = int(os.getenv("PUNYA_CHANNEL_ID"))
ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID"))
TIMEZONE = os.getenv("TIMEZONE")
API_URL = os.getenv("API_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
def timestamper(logger, log_method, event_dict):
    event_dict["timestamp"] = datetime.now(ZoneInfo(TIMEZONE)).isoformat()
    return event_dict

structlog.configure(
    processors=[
        timestamper,
        structlog.processors.add_log_level,
        structlog.processors.EventRenamer("message"),
        structlog.dev.ConsoleRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

log = structlog.get_logger()
bot = Client("alert_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Client("alert_app", api_id=API_ID, api_hash=API_HASH, plugins=dict(root="app_plugins"))

