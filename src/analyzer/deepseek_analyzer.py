from analyzer.analyzer_model import AnalyzerModel
from logger import logger
from utils import build_user_prompt, build_system_prompt

import requests

class DeepseekAnalyzer(AnalyzerModel):
    def __init__(self, config):
        super().__init__()
        self._config = config

    def analyze(self, data: list[str]) -> str:
        analyzer_config = self._config['llm'].analyzer
        model_provider_name, model_name = analyzer_config.split(',') if ',' in analyzer_config else ("", "")
        model_provider_name = model_provider_name.strip().lower()
        model_name = model_name.strip().lower()

        api_key = self._config['secrets'].get(model_provider_name, {}).get('api_key', "")

        model_info = self._config['llm'].models.get(model_provider_name, {}).get(model_name, {})
        base_url = model_info.get('base_url', "")
        temperature = model_info.get('temperature', 0.0)
        max_tokens = model_info.get('max_tokens', 2000)

        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(data)

        try:
            response = requests.post(
                url=base_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,  # Use chat model for faster summarization
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens  # Enough for structured bullets + trace
                }
            )
            response.raise_for_status()
            result = response.json()

            summary = result['choices'][0]['message']['content']
            return summary
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during Deepseek API call: {e}")
            raise