import asyncio
import os
import random
import numpy

from PIL import Image


class ImageServer:
    def __init__(self):
        self.flag: numpy.ndarray = None

    def initialize(self):
        with open('flag.bmp', 'rb') as f:
            with Image.open(f, mode='r') as img:
                self.flag = numpy.asarray(img)

    async def handler(self, reader, writer):
        try:
            writer.write(f"{self.flag.shape}\n".encode())
            writer.write("Input N >> \n".encode())
            try:
                N = int(await reader.readline())
            except ValueError:
                writer.write("Invalid N\n".encode())
                writer.close()
                return

            for _ in range(N):
                left_x = random.randint(0, self.flag.shape[1] - 1)
                right_x = min(random.randint(left_x + 1, left_x + self.flag.shape[1] // 10), self.flag.shape[1])
                top_y = random.randint(0, self.flag.shape[0] - 1)
                bottom_y = min(random.randint(top_y + 1, top_y + self.flag.shape[0] // 10), self.flag.shape[0])
                writer.write(f"{left_x}-{right_x}x{top_y}-{bottom_y}\n".encode())
                writer.write(bytes(self.flag[top_y:bottom_y, left_x:right_x]))

        finally:
            writer.close()

    async def listen_forever(self, host: str, port: int):
        server = await asyncio.start_server(self.handler, host, port)
        print(f"Server listened at {host}:{port}")
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    server = ImageServer()
    server.initialize()
    asyncio.run(server.listen_forever(os.environ['HOST'], int(os.environ['PORT'])))
