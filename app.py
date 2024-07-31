import asyncio
import logging
import os
import pickle

import aiohttp
import feedparser
from telegram import Bot

PICKLE_FILE = "seen_entries.pkl"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FEED_URL = os.getenv("FEED_URL")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def load_seen_entries():
    logger.info("Loading seen entries from pickle file")
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, "rb") as f:
            return pickle.load(f)
    logger.info("No seen entries file found, starting fresh")
    return set()


def save_seen_entries(seen_entries):
    logger.info("Saving seen entries to pickle file")
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(seen_entries, f)


async def get_feed_entries(feed_url):
    logger.info(f"Fetching feed entries from URL: {feed_url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(feed_url) as response:
            content = await response.text()
            feed = feedparser.parse(content)
            entries = feed.entries
            logger.info(f"Fetched {len(entries)} entries from feed")
            return [
                (entry.id, entry.title, entry.description, entry.link)
                for entry in entries
            ]


async def check_new_entries():
    logger.info("Checking for new entries")
    seen_entries = load_seen_entries()
    current_entries = await get_feed_entries(FEED_URL)
    new_entries = [entry for entry in current_entries if entry[0] not in seen_entries]

    # Reverse the list so that the newest entries are sent last
    new_entries.reverse()

    bot = Bot(token=BOT_TOKEN)

    if new_entries:
        logger.info(f"Found {len(new_entries)} new entries")
        for entry in new_entries:
            message = f"{entry[1]}\n\n{entry[2]}\n\n{entry[3]}"
            await bot.send_message(chat_id=CHAT_ID, text=message)
            seen_entries.add(entry[0])
    else:
        logger.info("No new entries found")

    save_seen_entries(seen_entries)


async def main():
    await check_new_entries()


if __name__ == "__main__":
    asyncio.run(main())
