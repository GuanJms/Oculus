# TODO: Test this class
from data_system._enums import TimeUnit
from data_system.base_structure.deque import TimeDeque
from data_system.containers.container_managers._container_manager import (
    ContainerManager,
)
from data_system.containers.cores import QueuePipeline


class TimeLagQueueManager(ContainerManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._asset = kwargs.get("asset", None)

    def add_lag_tracker(
        self, time_frame: int, time_unit: TimeUnit | str, lag=0, has_lag=False
    ):
        unit = TimeUnit.get(time_unit)
        if unit != TimeUnit.SECOND:  # TODO: add more time units later
            raise Exception("Only second time unit is supported for now")
        key = (time_frame, lag)
        time_frame_msd = int(time_frame * 1000)  # msd
        lag_msd = int(lag * 1000)
        if self.has_key(key):
            print(f"Key{key} already exists")
            return
        self.create_container(
            key,
            time_frame_msd=time_frame_msd,
            lag_msd=lag_msd,
            asset=self._asset,
            domains=self._domains,
            has_lag=has_lag,
        )
        print("Not recommended if extensively construct lag chain.")

    def inject(self, data, domains, meta=None):
        for container in self._containers.values():
            if (
                container.get_domains() == domains
            ):  # TODO: Redundant please check in the future
                container.inject(data)  # skipping meta for now
            else:
                print("Error in TimeLagQueueManager - FUNC inject")
                print(
                    f"Container domains: {container.get_domains()} not equal to {meta.get('domains')}"
                )

    def create_container(self, key, **kwargs):
        queue_pipeline = QueuePipeline(**kwargs)
        time_frame_msd = kwargs.get("time_frame_msd")
        has_lag = kwargs.get("has_lag", False)
        lag_msd = kwargs.get("lag_msd", 0)
        if has_lag:
            lag_queue = TimeDeque(max_time=lag_msd)
            main_queue = TimeDeque(max_time=time_frame_msd)
            queue_pipeline.add_queue_manager(lag_queue)
            queue_pipeline.add_queue_manager(main_queue)
        else:
            main_queue = TimeDeque(max_time=time_frame_msd)
            queue_pipeline.add_queue_manager(main_queue)
        domains = kwargs.get("domains", self._domains)
        queue_pipeline.set_domains(domains)
        self.set_container(
            key, queue_pipeline
        )  # Update the container domains automatically

    def get_lag_tracker(self, time_frame, lag=0):
        key = (time_frame, lag)
        queue_pipeline: QueuePipeline = self.get_container(key)
        if queue_pipeline:
            return queue_pipeline.get_last_queue()
        else:
            print(f"Key {key} not found in TimeLagQueueManager")
            return None
