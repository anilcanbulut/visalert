import asyncio
import random

from data.base_data_collector import BaseDataCollector
from telethon import TelegramClient

from logger import logger


class TelegramDataCollector(BaseDataCollector):
    def __init__(self, config):
        super().__init__()
        self._config = config
        self._client = None

    def _get_client(self):
        if self._client is None:
            api_id = self._config.get('secrets', {}).get('telegram', {}).get('api_id')
            api_hash = self._config.get('secrets', {}).get('telegram', {}).get('api_hash')
            self._client = TelegramClient("session", api_id, api_hash)
        return self._client

    def collect_data(self):
        telegram_info = self._config.get('sources', {}).selected_sources.get('telegram', {})
        last_n_messages = telegram_info.get('last_n_messages', 10)
        channels = telegram_info.get('channels', [])

        logger.debug(f"Channels to fetch: {channels}")

        client = self._get_client()
        messages = []

        async def _fetch():
            if not client.is_connected():
                phone = self._config.get('secrets', {}).get('telegram', {}).get('phone')
                await client.start(phone=phone)

            for channel in channels:
                delay = random.uniform(2, 5)
                await asyncio.sleep(delay)

                logger.debug(f"Fetching last {last_n_messages} messages from channel: {channel}...")
                msg_count = 0
                async for message in client.iter_messages(channel, limit=last_n_messages):
                    if message.text:
                        msg_count += 1
                        messages.append(message.text)
                logger.debug(f"Fetched {msg_count} messages from {channel}.")

        client.loop.run_until_complete(_fetch())

        return messages
