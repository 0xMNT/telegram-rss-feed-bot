# RSS Feed Checker and Telegram Notifier

![Python](https://img.shields.io/badge/python-3.12-blue) [![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)](https://core.telegram.org/bots/api)


This script periodically checks an RSS feed for new entries and sends updates to a specified Telegram chat. It is designed to run as a cron job and uses asynchronous operations to efficiently handle network requests.

## Features

* Fetches entries from an RSS feed.
* Sends new entries to a specified Telegram chat.
* Uses asynchronous operations for efficient network handling.
* Configurable via environment variables.
* Designed to run periodically using cron jobs.

## Prerequisites

* Python 3.7 or later
* Telegram bot token and chat ID (check Telegram botFather)
* Required Python packages (listed in requirements.txt)

## Installation

1. Clone the Repository

```bash
git clone https://github.com/0xMNT/telegram-rss-feed-bot.git
cd telegram-rss-feed-bot
```

2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Set Up Environment Variables

Set the following environment variables in your shell configuration file (e.g., .bashrc, .zshrc):

```bash
export TELEGRAM_BOT_TOKEN='your_bot_token'
export TELEGRAM_CHAT_ID='your_chat_id'
export FEED_URL='your_feed_url'
```

5. Set Up Cron Job

```bash
crontab -e
```
Cron jobs run in a minimal environment, so they do not automatically inherit environment variables that are set in your shell session, therefor we need to put the variables in the cronjob.

```bash
TELEGRAM_BOT_TOKEN='your_bot_token'
TELEGRAM_CHAT_ID='your_chat_id'
FEED_URL='your_feed_url'
``` 

Add the following line to run the script every 30 minutes
The logfile will be saved in the /root dir.

```bas
*/30 * * * * /root/telegram-rss-feed-bot/.venv/bin/python3.11 /root/telegram-rss-feed-bot/app.py >> logfile.log 2>&1
```


# Script Overview

## Main Components

* Environment Variables: The script uses TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to configure the Telegram bot. Set the FEED_URL as well.
* Seen Entries File: Entries already sent are stored in a pickle file (seen_entries.pkl).

## Functions

* load_seen_entries(): Loads the seen entries from the pickle file.
* save_seen_entries(seen_entries): Saves the seen entries to the pickle file.
* get_feed_entries(feed_url): Fetches entries from the RSS feed asynchronously.
* check_new_entries(): Checks for new entries and sends them to the Telegram chat.
* main(): Main function that runs the check_new_entries function.

## Asynchronous Operations

The script uses async and await to handle network requests and sending messages efficiently:

* get_feed_entries(feed_url): Asynchronously fetches RSS feed entries.
* check_new_entries(): Asynchronously sends messages to the Telegram chat.

## Error Handling

* Logs information using the logging module.
* Handles cases where the pickle file is not found and starts fresh.

# Usage

1. Ensure the environment variables are set.
2. Run the script manually to test:

```bash
python app.py
```

3. Set up the cron job to run the script periodically.

# Dockerize

## Usage

1. Build the Docker image using the following command:

```bash
docker build -t <image-name> .
```

2. Run the Docker container with the required environment variables for Telegram Bot Token, Chat ID and RSS Feed URL.

``` bash
docker run -d --name <container-name> \
    -e TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN \
    -e TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID \
    -e FEED_URL=$FEED_URL \
    <image-name>
```
