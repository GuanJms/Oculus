import asyncio
import json
import time
from typing import Optional

from kafka import KafkaConsumer

from data_system.connection.live_stream.kafka_handler import KafkaHandler


class StreamReceiverConsumer:
    def __init__(
        self,
        topic,
        bootstrap_servers,
        max_poll_records,
        value_deserializer,
        auto_offset_reset,
        injector=None,
        *topics,
        **configs
    ):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            max_poll_records=max_poll_records,
            value_deserializer=value_deserializer,
            auto_offset_reset=auto_offset_reset,
        )
        self.value_deserializer = value_deserializer
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.max_poll_records = max_poll_records
        self.value_deserializer = value_deserializer
        self.auto_offset_reset = auto_offset_reset
        self.handler: Optional[KafkaHandler] = None

        # Time Simulation Setting
        self.slow_mode = configs.get("slow_mode", False)
        self.slow_factor = configs.get("slow_factor", 1)
        if self.slow_factor <= 0:
            raise ValueError("Slow factor must be greater than 0")
        self.slow_time = 0.001 / self.slow_factor
        self.verbose = configs.get("verbose", False)

    def __iter__(self):
        return self.consumer

    def run(self):
        if self.handler is None:
            raise ValueError("Handler is not set")
        for message in self.consumer:
            self.send(data=message)

    def set_handler(self, handler: KafkaHandler):
        self.handler = handler

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def send(self, data):
        if self.verbose:
            print(json.loads(data.value))
        if self.handler is not None:
            self.handler.send(data)
        if self.slow_mode:
            time.sleep(self.slow_time)
