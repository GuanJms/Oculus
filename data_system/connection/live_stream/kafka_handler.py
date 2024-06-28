import json
import threading

from data_system.process.domain_distributors import AssetDistributor


class KafkaHandler:
    def __init__(self, system_distributor: AssetDistributor, lock: threading.Lock = None):
        self.system_distributor = system_distributor
        self.lock = lock

    def send(self, message):
        json_message = json.loads(message.value)
        if self.lock:
            with self.lock:
                self.system_distributor.distribute(json_message)
        else:
            print("No lock provided")
            self.system_distributor.distribute(json_message)
