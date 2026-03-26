import json
import time

from config.config_reader import ConfigReader
from data.data_collector_factory import DataCollectorFactory
from analyzer.analyzer_model_factory import AnalyzerModelFactory
from notifier.telegram_notifier import TelegramNotifier
from logger import logger
from utils import process_messages, format_alerts

class Main:
    def __init__(self):
        self._init()

    def _init(self):
        self._configs = ConfigReader().get_configs()
        self._data_collectors = DataCollectorFactory.create_data_collector(self._configs)
        self._analyzer = AnalyzerModelFactory.create_analyzer_model(self._configs)
        self._notifier = TelegramNotifier(self._configs)

    def start(self):
        logger.info("Starting the application...")
        run_period = self._configs.get('base', {}).run_period
        while True:
            try:
                self._run()
            except Exception as e:
                logger.error(f"Error during run: {e}")
            logger.info(f"Sleeping for {run_period} seconds...")
            time.sleep(run_period)

    def _run(self):
        all_messages = []
        for data_collector in self._data_collectors:
            messages = data_collector.collect_data()
            all_messages.extend(messages)

        logger.debug(f"Collected {len(all_messages)} messages in total.")

        processed_messages = process_messages(all_messages)
        analysis_result = self._analyzer.analyze(processed_messages)

        # logger.debug(f"\nFetched messages:")
        # for msg in processed_messages:
        #     logger.debug(f"- {msg}")

        if not analysis_result or analysis_result.strip().upper() == "NO":
            logger.info("No alerts found in this run.")
            return

        try:
            alerts = json.loads(analysis_result).get("alerts", [])
        except (json.JSONDecodeError, TypeError):
            logger.error(f"Failed to parse analysis result: {analysis_result}")
            return

        if alerts:
            message = format_alerts(alerts)
            self._notifier.notify(message)
            logger.info(f"Sent alert notification with {len(alerts)} alert(s)")
        else:
            logger.info("No alerts found in this run.")


if __name__ == "__main__":
    main = Main()
    main.start()