from config.config_reader import ConfigReader
from data.telegram_data_collector import TelegramDataCollector
from notifier.telegram_notifier import TelegramNotifier

c = ConfigReader()
notifier = TelegramNotifier(c.get_configs())    

notifier.notify("TESTTT")