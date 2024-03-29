class MessageProcessor:
    def process(self, message):
        raise NotImplementedError

class TextMessageProcessor(MessageProcessor):
    def process(self, message):
        print(f"Processing text message: {message}")

class ImageMessageProcessor(MessageProcessor):
    def process(self, message):
        print(f"Processing image message: {message}")

class ProcessorFactory:
    @staticmethod
    def get_processor(message_type):
        if message_type == 'text':
            return TextMessageProcessor()
        elif message_type == 'image':
            return ImageMessageProcessor()
        else:
            raise ValueError("Unknown message type")


import threading

def process_message(message_type, message_content):
    processor = ProcessorFactory.get_processor(message_type)
    processor.process(message_content)

# Example messages
messages = [
    ('text', "Hello, World!"),
    ('image', "image1.png"),
    ('text', "Another message"),
    ('image', "image2.png")
]

threads = []
for message_type, message_content in messages:
    thread = threading.Thread(target=process_message, args=(message_type, message_content))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
