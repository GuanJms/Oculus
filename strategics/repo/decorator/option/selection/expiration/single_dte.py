# from utils.global_id import GlobalComponentIDGenerator
# from strategics.repo import SignalGenerator
#
#
# class SingleDTESignalGenerator(SignalGenerator):
#
#     def __init__(self, msd: int, quote_date: int):
#         super().__init__()
#         self._signal_name = SingleDTESignalGenerator.__name__
#         self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
#
#     def generate_signal(self):
#         pass
#
# #
# #
# # class SingleDTESignalCoordinator(ExecutionSignalCoordinator):
# #     def __init__(self):
# #         super().__init__()
# #         self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
# #         self._signal_name = SingleDTESignalGenerator.__name__
# #
# #     def create_execution_signal(self):
# #         signal_generation = SingleDTESignalGenerator()
