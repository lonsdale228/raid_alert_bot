import datetime
import os
from zoneinfo import ZoneInfo

import aiohttp
from loader import API_URL, TIMEZONE, log, ALERT_CHANNEL_ID

tz = ZoneInfo(TIMEZONE)

alert_sent = False
current_alert = None

if os.name == "nt":
    API_URL = API_URL
else:
    API_URL = "http://raid_api:5000/data"

async def check_air_raid(bot):
    global alert_sent, current_alert
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL) as resp:
                js = await resp.json()
                time = datetime.datetime.now(tz).strftime("%H:%M:%S")

                alert = 18 in js

                if alert and not alert_sent:
                    text = f"❗️{time} — Повітряна тривога!"
                    await bot.send_message(chat_id=ALERT_CHANNEL_ID, text=text, disable_notification=False)
                    alert_sent = not alert_sent
                    await log.ainfo(text)
                    current_alert = True

                if not alert and alert_sent:
                    text = f"🟢 {time} — Відбій повітряної тривоги!"
                    await bot.send_message(chat_id=ALERT_CHANNEL_ID, text=text,
                                           disable_notification=False)
                    alert_sent = not alert_sent
                    await log.ainfo(text)
                    current_alert = False

        except aiohttp.client_exceptions.ClientConnectorError:
            await log.aexception("Cannot connect to Raid Alert api server!")
        except Exception as e:
            await log.aexception(e)