import os
import json
from typing import ClassVar, Optional, TextIO


class ConfigurationManager:
    _configure_folder_path: ClassVar[str] = os.path.join(os.path.dirname(__file__), 'configuration_files')
    _path_config: ClassVar[dict] = {}
    _raw_traded_quote_config: ClassVar[dict] = {}
    _MSD_COL_NAME: Optional[str] = None
    _MSD_COL_NAME_SECONDARY: Optional[str] = None
    _root_system: Optional[str] = None
    _quote_folder_name: Optional[str] = None
    _initialized_num: int = 0

    @classmethod
    def get_initialized_num(cls) -> int:
        return cls._initialized_num


    @classmethod
    def load_configurations(cls):
        """Reads all JSON configuration files in the configuration folder and    updates the class-level configuration
        dictionaries."""
        cls._initialized_num += 1
        for filename in os.listdir(cls._configure_folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(cls._configure_folder_path, filename)
                with open(file_path, 'r') as config_file:
                    cls._run_configure_folder(filename, config_file)

    @classmethod
    def _run_configure_folder(cls, filename: str, config_file: TextIO):
        if 'path_config' in filename:
            cls._run_path_config(config_file)
        if 'raw_traded_quote_config' in filename:
            cls._run_raw_traded_quote_config(config_file)

    @classmethod
    def get_root_path(cls):
        """Returns the root path."""
        cls._check_initialized()
        return cls._configure_folder_path

    @classmethod
    def get_path_config(cls):
        """Returns the path configuration."""
        cls._check_initialized()
        return cls._path_config

    @classmethod
    def get_raw_traded_quote_config(cls):
        """Returns the raw traded quote configuration."""
        cls._check_initialized()
        return cls._raw_traded_quote_config

    @classmethod
    def get_MSD_COL_NAME(cls) -> Optional[str]:
        """Returns the MSD column name."""
        cls._check_initialized()
        if len(cls._raw_traded_quote_config) == 0:
            raise ValueError('Missing raw_traded_quote_config')
        if cls._MSD_COL_NAME is None:
            raise ValueError('Missing MSD_COL_NAME in raw_traded_quote_config')
        return cls._MSD_COL_NAME

    @classmethod
    def get_MSD_COL_NAME_SECONDARY(cls) -> Optional[str]:
        """Returns the secondary MSD column name."""
        cls._check_initialized()
        if len(cls._raw_traded_quote_config) == 0:
            raise ValueError('Missing raw_traded_quote_config')
        if cls._MSD_COL_NAME_SECONDARY is None:
            raise ValueError('Missing MSD_COL_NAME_SECONDARY in raw_traded_quote_config')
        return cls._MSD_COL_NAME_SECONDARY

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

    @classmethod
    def _check_initialized(cls):
        if cls._initialized_num == 0:
            cls.load_configurations()

    @classmethod
    def get_quote_folder_name(cls) -> Optional[str]:
        """Returns the quote folder name."""
        cls._check_initialized()
        if cls._quote_folder_name is None:
            raise ValueError('Missing quote_folder_name in path_config')
        return cls._quote_folder_name

    @classmethod
    def get_root_system(cls):
        cls._check_initialized()
        if cls._root_system is None:
            raise ValueError('Missing root_system in path_config')
        return cls._root_system
