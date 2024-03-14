from typing import Set, List

from execution_module.strategy_section_module.combo_section import ComboSection
from global_component_id_generator import GlobalComponentIDGenerator
from section import Section
from status_module.execution_status_module.strategy_section_status import StrategySectionStatus
from status_module.execution_status_module.strategy_section_status_info import StrategySectionStatusInfo


class StrategySection(Section):

    def __init__(self):
        super().__init__()
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.combo_section_list: List[ComboSection] = []
        raise NotImplementedError

    def refresh_status(self):
        for combo_section in self.combo_section_list:
            combo_section.refresh_status()
        raise NotImplementedError
