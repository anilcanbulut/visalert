from analyzer.analyzer_model import AnalyzerModel
from analyzer.deepseek_analyzer import DeepseekAnalyzer

class AnalyzerModelFactory:
    @staticmethod
    def create_analyzer_model(configs) -> AnalyzerModel:
        analyzer_config = configs['llm'].analyzer
        model_provider_name, model_name = analyzer_config.split(',') if ',' in analyzer_config else ("", "")
        if model_provider_name.strip().lower() == "deepseek":
            return DeepseekAnalyzer(configs)
        else:
            raise ValueError(f"Unsupported analyzer model provider: {model_provider_name}")