from _enums import TimelineType, OperationMode


def convert_timeline_type_to_operation_mode(timeline_type: TimelineType) -> OperationMode:
    if timeline_type == TimelineType.SIMULATION:
        return OperationMode.BACKTEST
