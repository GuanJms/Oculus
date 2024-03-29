import threading
import queue
import time

class Listener(threading.Thread):
    def __init__(self, msg_queue):
        super().__init__()
        self.msg_queue = msg_queue
        self.daemon = True  # Allows the thread to be killed when the main program exits

    def run(self):
        while True:
            message = self.msg_queue.get()
            if message == "STOP":
                print("Listener stopping.")
                break
            print(f"Received: {message}")
            self.msg_queue.task_done()

class Sender(threading.Thread):
    def __init__(self, msg_queue):
        super().__init__()
        self.msg_queue = msg_queue
        self.daemon = True

    def run(self):
        for i in range(10):  # Example: Send 10 messages then stop
            time.sleep(0.1)  # Simulate time-consuming work
            self.msg_queue.put(f"Message {i}")
        # self.msg_queue.put("STOP")  # Signal the listener to stop

# Create a shared queue for messages
message_queue = queue.Queue()


# Start the listener and sender threads
listener = Listener(message_queue)
sender = Sender(message_queue)

listener.start()
sender.start()

# Wait for all items in the queue to be processed
sender.join()

print("Main program completed.")
