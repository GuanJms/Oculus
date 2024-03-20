from typing import Dict


class GlobalComponentIDGenerator:
    _instance_last_id: int = 0
    _class_last_id: int = 0
    _class_id_dict: Dict[str, int] = {}

    @classmethod
    def generate_unique_id(cls, instance_class_name: str, instance_id: int):
        cls._instance_last_id += 1
        unique_class_id = cls._get_class_id(instance_class_name)
        unique_id_str = f"{instance_class_name}-{str(unique_class_id)}-{str(cls._instance_last_id)}-{instance_id}"
        return unique_id_str

    @classmethod
    def generate_unique_class_id(cls, class_name: str):
        return cls._get_class_id(class_name)

    @classmethod
    def _get_class_id(cls, class_name: str):
        if class_name in cls._class_id_dict:
            return cls._class_id_dict[class_name]
        else:
            cls._class_last_id += 1
            cls._class_id_dict[class_name] = cls._class_last_id
            return cls._class_last_id

    @classmethod
    def get_last_id(cls):
        return cls._instance_last_id

