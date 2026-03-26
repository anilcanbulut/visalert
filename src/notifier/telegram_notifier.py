import requests

from logger import logger


class TelegramNotifier:
    def __init__(self, config):
        self._config = config

    def notify(self, message: str):
        bot_token = self._config.get('secrets', {}).get('telegram', {}).get('bot_api')
        channel = self._config.get('base', {}).get('telegram_notification_channel', '@visalertt')

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = requests.post(url, json={
            "chat_id": channel,
            "text": message,
        })

        if response.ok:
            logger.info("Notification sent successfully.")
        else:
            logger.error(f"Failed to send notification: {response.text}")
