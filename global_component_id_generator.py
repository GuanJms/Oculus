class GlobalComponentIDGenerator:
    _last_id = 0

    @classmethod
    def generate_unique_id(cls, instance_class_name: str, instance_id: int):
        cls._last_id += 1
        unique_id_str = f"{instance_class_name}-{str(cls._last_id)}-{instance_id}"
        return unique_id_str

    @classmethod
    def get_last_id(cls):
        return cls._last_id
