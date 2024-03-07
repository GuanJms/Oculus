from strategy_module.combo_module.combo_rule import ComboRule


class SynchronizeComboRule(ComboRule):
    """
    SynchronizeComboRule is a empty entity for extend ComboRule that will be decorated by SynchronizeRule.
    """

    def __init__(self):
        super().__init__()
        self.combo_name = 'Synchronize Combo'
        self.combo_type = 'synchronize_combo'

