import asyncio
import threading
import time
from collections import deque
import multiprocessing

from kafka import KafkaConsumer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from data_system.base_structure.deque.acc_deque import AccDeque
from data_system.connection.live_stream.kafka_consumer import StreamReceiverConsumer
import json

from data_system.process.pipelines.option_data_pipeline import OptionDataPipeline
from data_system.containers.cores import QueuePipeline


# TODO: Rewrite the plot test
def count_nodes(option_multi_ticker_container: MultiTickerContainerManager):
    while True:
        tesla_container: OptionContainerManager = (
            option_multi_ticker_container.get_container("TSLA")
        )
        print(" --------- Node count --------- ")
        for (
            key,
            value,
        ) in tesla_container.get_containers().items():  # type: str, QueuePipeline
            print(f"key: {key}, node count: {value.get_accumulated_size()}")
        time.sleep(1)
        # print("count_nodes: ", option_q)
        # if option_q is None:
        #     print("No option queue found")
        #     return
        # print(option_q._accumulator)


# def animate(queue, lock):
#     queue: OptionContainerManager
#     fig, axs = plt.subplots(3, 1, figsize=(10, 8))  # Adjust figsize as needed
#     while True:
#         with lock:
#             keys = sorted(queue.get_option_keys())
#             if len(keys) > 3:
#                 break
#             # Create 3 subplots
#             for idx, key in enumerate(keys):
#                 pipe: QueuePipeline = queue.get_container(key)
#                 acc: AccDeque = pipe.accumulator
#
#                 # Get timestamp data from nodes from accumulator
#                 x_vals = acc.get_attribute_to_list("timestamp")
#                 y_vals = acc.get_attribute_to_list("price")
#
#                 axs[idx].cla()
#                 axs[idx].plot(x_vals, y_vals, label="Price")
#                 print(len(x_vals), len(y_vals))
#                 axs[idx].legend(loc="upper left")
#                 axs[idx].set_title(f"Plot {idx + 1} for key: {key}")
#             plt.tight_layout()
#             plt.pause(0.01)


def animate(i, queue, lock, fig, axs):
    queue: OptionContainerManager
    with lock:
        keys = sorted(queue.get_option_keys())
        if len(keys) > 3:
            return
        # Create 3 subplots
        for idx, key in enumerate(keys):
            pipe: QueuePipeline = queue.get_container(key)
            acc: AccDeque = pipe.accumulator

            # Get timestamp data from nodes from accumulator
            x_vals = acc.get_attribute_to_list("timestamp")
            y_vals = acc.get_attribute_to_list("price")

            axs[idx].cla()
            axs[idx].plot(x_vals, y_vals, label="Price")
            print(len(x_vals), len(y_vals))
            axs[idx].legend(loc="upper left")
            axs[idx].set_title(f"Plot {idx + 1} for key: {key}")


def main():
    plt.style.use("fivethirtyeight")
    c = StreamReceiverConsumer(
        topic="TSLA_stream",
        bootstrap_servers="localhost:9092",
        max_poll_records=100,
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset="earliest",  # ,'smallest'
    )

    option_multi_ticker_container = MultiTickerContainerManager()
    print("ID of option_multi_ticker_container: ", id(option_multi_ticker_container))

    option_multi_ticker_container.create_container(
        "TSLA", security_type="OPTION", auto_add=True, accumulated=True
    )

    pipe = OptionDataPipeline(steps=[], domains=None, verbose=False)
    pipe.trade_injector.price_manager = option_multi_ticker_container
    print("Starting consumer")
    c.set_pipeline(pipe)

    print("option_multi_ticker_container:", option_multi_ticker_container)
    tesla_queue = option_multi_ticker_container.get_container("TSLA")

    # Set up the animation
    lock = threading.Lock()
    t1 = threading.Thread(target=c.run, args=())
    # t2 = threading.Thread(target=count_nodes, args=(option_multi_ticker_container,))
    t1.start()
    fig, axs = plt.subplots(20, 1, figsize=(5, 3))  # Adjust figsize as needed
    ani = FuncAnimation(
        plt.gcf(), animate, interval=200, fargs=(tesla_queue, lock, fig, axs)
    )
    plt.tight_layout()
    plt.show()
    # t2.start()
    t1.join()
    # t2.join()


if __name__ == "__main__":
    main()
