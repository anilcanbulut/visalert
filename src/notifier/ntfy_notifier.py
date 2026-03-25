import requests

from logger import logger


class NtfyNotifier:
    def __init__(self, config):
        self._config = config

    def notify(self, message: str):
        ntfy_config = self._config.get('base', {})
        server = ntfy_config.get('ntfy_server', 'https://ntfy.sh')
        topic = ntfy_config.get('ntfy_topic', '')

        if not topic:
            logger.error("ntfy topic is not configured in base.yaml")
            return

        url = f"{server}/{topic}"
        response = requests.post(url, data=message.encode('utf-8'), headers={
            "Title": "Visa Alert",
            "Priority": "high",
            "Tags": "warning"
        })

        if response.ok:
            logger.info("ntfy notification sent successfully.")
        else:
            logger.error(f"Failed to send ntfy notification: {response.status_code} {response.text}")
