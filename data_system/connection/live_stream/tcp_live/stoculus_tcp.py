import websockets
import asyncio
from multiprocessing import Queue

class StoculusTCPServer:
    def __init__(self, queue):
        self.port = 1777
        self.q: Queue = queue

    async def listen(self, websocket, path):
        try:
            async for message in websocket:
                if message is None or message == "" or message == "None":
                    continue
                print(f"Received message: {message}")
                # self.q.put(message)
                print("Queue size: ", self.q.qsize())

        except Exception as e:
            print(f"Error: {e} 1323")
        await asyncio.sleep(0)

    def run(self):
        start_server = websockets.serve(self.listen, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()