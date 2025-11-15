import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from alert_monitoring import check_air_raid
from bpla_monitor import get_bpla_info
from loader import app, bot, log, TIMEZONE
from pyrogram import compose

from send_punya import send_punya


async def run_scheduler():
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(check_air_raid, IntervalTrigger(seconds=2), args=(bot,))
    scheduler.add_job(send_punya, CronTrigger(hour=15), args=(bot,))
    # scheduler.add_job(get_bpla_info, IntervalTrigger(seconds=20, jitter=5), args=(bot,))
    scheduler.start()
    await log.ainfo("Scheduler started!")


async def main():
    apps = [app, bot]

    await run_scheduler()

    await log.ainfo("Started!")

    async with app:
        await app.send_message(chat_id='me', text="Raid alert bot started!")

    await compose(apps)



if __name__ == "__main__":
    asyncio.run(main())