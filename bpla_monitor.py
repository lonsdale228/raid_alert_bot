import re

import aiohttp

from loader import ALERT_CHANNEL_ID

BPLA_API_URL = "https://mapa.com.ua/actual_data.json"

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}

regex_filter_city = r"оде[сщ]|чорномор|сов[іi]н[йь]|бурлач"

async def get_bpla_info(bot):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BPLA_API_URL) as resp:
            js = await resp.json()
            for region in js["data"]:
                if bool(re.search(regex_filter_city, region["target"], re.IGNORECASE)):
                    text = fr"{region['message']}"
                    await bot.send_message(chat_id=ALERT_CHANNEL_ID, text=text, disable_notification=False)
