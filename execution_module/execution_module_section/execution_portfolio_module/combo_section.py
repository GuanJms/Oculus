from typing import List

from execution_module.execution_module_section.execution_portfolio_module.leg_section import LegSection
from global_component_id_generator import GlobalComponentIDGenerator
from section import Section


class ComboSection(Section):

    def __init__(self):
        super().__init__()
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._leg_section_list: List[LegSection] = []

    def refresh_status(self):
        raise NotImplementedError
