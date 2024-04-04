import os
import json
from typing import Optional, TextIO


def update_configure(func):
    def wrapper(*args, **kwargs):
        cls = args[0]
        cls._check_initialized()
        return func(*args, **kwargs)
    return wrapper


class ConfigurationManager:
    _configure_folder_path: str = os.path.join(os.path.dirname(__file__), 'configuration_files')
    _root_system: Optional[str] = None
    _domain_path_dict: dict = {}
    _path_config: dict = {}
    _initialized: bool = False


    @classmethod
    def load_configurations(cls):
        """Reads all JSON configuration files in the configuration folder and    updates the class-level configuration
        dictionaries."""
        cls._initialized = True
        for filename in os.listdir(cls._configure_folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(cls._configure_folder_path, filename)
                with open(file_path, 'r') as config_file:
                    cls._run_configure_folder(filename, config_file)

    @classmethod
    def _check_initialized(cls):
        if not cls._initialized:
            cls.load_configurations()

    @classmethod
    def _run_configure_folder(cls, filename: str, config_file: TextIO):
        if 'path_config' in filename:
            cls._run_path_config(config_file)
        if 'raw_traded_quote_config' in filename:
            cls._run_raw_traded_quote_config(config_file)



    @classmethod
    @update_configure
    def get_root_system(cls):
        cls._check_initialized()
        if cls._root_system is None:
            raise ValueError('Missing root_system in path_config')
        return cls._root_system

    @classmethod
    def _run_path_config(cls, config_file):
        config_data = json.load(config_file)
        cls._path_config.update(config_data)
        cls._root_system = config_data.get('root_system', None)
        cls._quote_folder_name = config_data.get('quote_folder_name', None)

    @classmethod
    def _run_raw_traded_quote_config(cls, config_file):
        config_data = json.load(config_file)
        cls._raw_traded_quote_config.update(config_data)
        cls._MSD_COL_NAME = config_data.get('MSD_COL_NAME', None)
        cls._MSD_COL_NAME_SECONDARY = config_data.get('MSD_COL_NAME_SECONDARY', None)

