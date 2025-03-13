import os

import tgcrypto
import asyncio
import datetime
import random
from pyrogram import filters, enums, compose, Client
import pyrogram
from pyrogram.types import Message
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import pytz

timezone = 'Europe/Kyiv'

tz = pytz.timezone(timezone)


def timetz(*args):
    return datetime.datetime.now(tz).timetuple()


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.Formatter.converter = timetz

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

punya_id = -1002128958498

# TEST_CHAT_ID = -1001239857869
ALERT_CHANNEL_ID = -1002070271876

API_URL = "https://api.alerts.in.ua/v1/alerts/active.json"
NEW_API_KEY = os.getenv("NEW_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
alert_sended = False

current_alert = None

def get_alert_status(js_list):
    for reg in js_list['alerts']:
        if "одес" in reg['location_title'].lower():
            return True
    return False


async def check_air_raid(bot):
    global alert_sended, cancel_sended, current_alert
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL + f"?token={NEW_API_KEY}") as resp:
                js = await resp.json()
                time = datetime.datetime.now(tz).strftime("%H:%M:%S")

                alert = get_alert_status(js)

                if alert and not alert_sended:
                    text = f"❗️{time} — Повітряна тревога!"
                    await bot.send_message(chat_id=ALERT_CHANNEL_ID, text=text, disable_notification=False)
                    alert_sended = not alert_sended
                    logger.info(text)
                    current_alert = True

                if not alert and alert_sended:
                    text = f"🟢 {time} — Відбій повітрянної тревоги!"
                    await bot.send_message(chat_id=ALERT_CHANNEL_ID, text=text,
                                           disable_notification=False)
                    alert_sended = not alert_sended
                    logger.info(text)
                    current_alert = False

        except aiohttp.client_exceptions.ClientConnectorError:
            logger.exception("Cannot connect to Raid Alert api server!")


# @app.on_message(filters.chat(CHAT_ID), filters.text)
# async def on_monitor_msg(client, message: Message):
#     for keyword in KEY_WORDS:
#         if keyword in message.text:
#             text = "⚠️ " + message.text.html + " \n\nFrom Monitor"
#             await bot.send_message(ALERT_CHANNEL_ID,
#                                    text=text,
#                                    entities=message.entities,
#                                    parse_mode=enums.ParseMode.HTML,
#                                    disable_notification=True,
#                                    disable_web_page_preview=True)
#             logger.info(text)
#         break
#     logger.debug(message.text.html)


async def send_punya(bot):
    text = random.choice([
        "На превеликий жаль путін сьогодні не здох(",
        "Сьогодні, на жаль, він ще не вмер",
        "Коли вже пиня вмре? На всесвітній жаль не сьогодні...",
        "Шкода, що путін сьогодні не помер",
        "Хочеться вірити, що путін помер, але на жаль цього не сталося",
        "Прикро, що путін все ще тут",
        "вдалий день для того, щоб путін помер, але не пощастило:(",
        "Сьогодні важко зрозуміти, чому путін ще не вмер",
        "На жаль, путін не помер, хоча всі цього бажають",
        "розчарування, шо путін не помер",
        "Шкода, що путін все ще серед нас",
        "Надія на те, щоб путін помер, сьогодні не збулася",
        "На жаль, путін все ще живий"
    ])
    await bot.send_message(punya_id, text)


async def main():
    global current_alert
    app = pyrogram.Client(name="userBot2323", parse_mode=enums.ParseMode.HTML)
    bot = pyrogram.Client(bot_token=BOT_TOKEN, name='botik')

    # KEY_WORDS = ["Одес", "Одещ", "Чорноморськ"]
    CHATS_INFO = [
        -1001641260594,
        -1001223955273
    ]



    @app.on_message(filters.chat(CHATS_INFO) & filters.text & filters.regex(r'[Оо]дес[а-я]*|[Чч]орномор'))
    async def on_monitor_msg(client: Client, message: Message):
        chat = await client.get_chat(message.chat.id)
        text = "⚠️ " + message.text.html + f' \n\n<a href="{message.link}">{chat.title}</a>'
        await bot.send_message(ALERT_CHANNEL_ID,
                               text=text,
                               parse_mode=enums.ParseMode.HTML,
                               disable_notification=True,
                               disable_web_page_preview=True)
        logger.info(text)
        logger.debug(message.text.html)

    scheduler = AsyncIOScheduler(timezone=timezone)
    scheduler.add_job(check_air_raid, "interval", seconds=7, args=(bot,))
    scheduler.add_job(send_punya, "cron", hour=15, args=(bot,))
    scheduler.start()

    logger.info('Running successfully!')

    apps = [
        app,
        bot
    ]

    await compose(apps)

    @app.on_message(filters.chat(CHATS_INFO) & filters.text & filters.regex(r'\b[Зз]агроза\b|\b[Бб]алістика\b|\b[Рр]акетн\w*\b'))
    async def on_warning(client: Client, message: Message):
        if current_alert:
            await bot.send_message(ALERT_CHANNEL_ID,
                                   text=text,
                                   parse_mode=enums.ParseMode.HTML,
                                   disable_notification=True,
                                   disable_web_page_preview=True)

asyncio.run(main())
