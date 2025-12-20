import re

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from loader import ALERT_CHANNEL_ID, app, log

CHATS_INFO = [
    -1001641260594, # @war_monitor
    -1001223955273, # @kpszsu
]

regex_filter_city = r"оде[сщ]|чорномор|сов[іi]н[йь]|бурлач|для\s*всіх\s*регіонів"
regex_critical = r"баліст|ка[бр]|кал[іi]б|г[іi]перзв|киндж|БпЛА|авіац\s*засоб\s*ураж"

@app.on_message(filters.chat(CHATS_INFO) & filters.text & filters.regex(regex_filter_city, re.IGNORECASE))
async def on_monitor_msg(client: Client, message: Message):
    chat = await client.get_chat(message.chat.id)
    text = "⚠️ " + message.text.html + f' \n\n<a href="{message.link}">{chat.title}</a>'

    critical = bool(re.search(regex_critical, message.text))

    await app.send_message(ALERT_CHANNEL_ID,
                           text=text,
                           parse_mode=enums.ParseMode.HTML,
                           disable_notification=not critical,
                           disable_web_page_preview=True)
    await log.ainfo(text)
    await log.adebug(message.text.html)