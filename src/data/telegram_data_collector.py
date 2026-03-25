from data.base_data_collector import BaseDataCollector
from telethon import TelegramClient

from logger import logger

class TelegramDataCollector(BaseDataCollector):
    def __init__(self, config):
        super().__init__()
        self._config = config

    def collect_data(self):
        api_id = self._config.get('secrets', {}).get('telegram', {}).get('api_id')
        api_hash = self._config.get('secrets', {}).get('telegram', {}).get('api_hash')

        telegram_info = self._config.get('sources', {}).selected_sources.get('telegram', {})
        last_n_messages = telegram_info.get('last_n_messages', 10)
        channels = telegram_info.get('channels', [])

        logger.debug(f"Channels to fetch: {channels}")

        session_name = telegram_info.get('session_name', 'session')
        client = TelegramClient(session_name, api_id, api_hash)

        messages = []

        async def _fetch():
            await client.start()
            for channel in channels:
                logger.debug(f"Fetching last {last_n_messages} messages from channel: {channel}...")
                msg_count = 0
                async for message in client.iter_messages(channel, limit=last_n_messages):
                    if message.text:
                        msg_count += 1
                        messages.append(message.text)
                logger.debug(f"Fetched {msg_count} messages from {channel}.")
                msg_count = 0
            await client.disconnect()

        with client:
            client.loop.run_until_complete(_fetch())

        return messages
