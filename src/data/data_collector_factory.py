from data.base_data_collector import BaseDataCollector
from data.telegram_data_collector import TelegramDataCollector

class DataCollectorFactory:
    @staticmethod
    def create_data_collector(configs) -> list[BaseDataCollector]:
        data_collectors = []
        for source_name in configs['sources'].selected_sources:
            if source_name == "telegram":
                data_collectors.append(TelegramDataCollector(configs))
            else:
                raise ValueError(f"Unsupported source: {source_name}")
        return data_collectors