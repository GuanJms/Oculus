from typing import List, Any, Dict


def check_attribute_exist(attributes: List[Any], args: Dict):
    error_attrs = []
    for attr in attributes:
        if args.get(attr, None) is None:
            error_attrs.append()
    if len(error_attrs) != 0:
        raise AttributeError(f"Attributes {error_attrs} are None")