import yaml
import os

from config.config_templates import *
from utils import get_project_root
from logger import logger

class ConfigReader:
    def __init__(self):
        self._config_folder_path = os.path.join(get_project_root(), "configs")
        self._configs = {}

        self._read_configs()
    
    def _read_configs(self):
        logger.debug("Reading configuration files...")
        self._configs['sources'] = self._load_sources_config()
        self._configs['secrets'] = self._load_secrets_config()
        self._configs['llm'] = self._load_llm_config()
        self._configs['countries'] = self._load_countries_config()
        self._configs['base'] = self._load_base_config()

    def get_configs(self):
        return self._configs

    def _read_config(self, config_file_name):
        with open(os.path.join(self._config_folder_path, config_file_name), 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _load_secrets_config(self):
        logger.info("Loading secrets configuration...")
        secrets_config = self._read_config("secrets.yaml")
        return secrets_config

    def _load_sources_config(self):
        logger.info("Loading sources configuration...")
        sources_template = Sources()
        sources_template.selected_sources = {}
        sources_config = self._read_config("sources.yaml")

        for source_name, source_config in sources_config.get("sources", {}).items():
            is_enabled = source_config.get("enable", False)
            if is_enabled:
                cfg = source_config.get("info", {})

                sources_template.selected_sources[source_name] = cfg
        
        return sources_template

    def _load_llm_config(self):
        logger.info("Loading LLM configuration...")
        llm_template = llm()
        llm_config = self._read_config("llm.yaml")

        llm_template.analyzer = llm_config.get("analyzer", "")
        llm_template.models = llm_config.get("models", {})

        return llm_template

    def _load_countries_config(self):
        logger.info("Loading countries configuration...")
        countries_template = Countries()
        countries_config = self._read_config("countries.yaml")

        countries_template.country_list = countries_config.get("countries", [])

        return countries_template

    def _load_base_config(self):
        logger.info("Loading base configuration...")
        base_template = Base()
        base_config = self._read_config("base.yaml")

        base_template.run_period = base_config.get("run_period", 600) # Default to 10 minutes if not specified

        return base_template