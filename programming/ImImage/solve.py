import asyncio
import os

import numpy
from PIL import Image


async def main():
    N = 10000
    reader, writer = await asyncio.open_connection(os.environ['HOST'], os.environ['PORT'])
    shape = eval(await reader.readline())
    print("shape", shape)
    buf = numpy.zeros(shape, dtype=numpy.uint8)
    await reader.readline()  # Input N >>
    writer.write(f"{N}\n".encode())
    for _ in range(N):
        line = await reader.readline()
        tokens = line.split(b'x')
        top_y, bottom_y = map(int, tokens[1].split(b'-'))
        left_x, right_x = map(int, tokens[0].split(b'-'))
        snippet = await reader.readexactly(n=(right_x - left_x) * (bottom_y - top_y))
        idx = 0
        for y in range(top_y, bottom_y):
            for x in range(left_x, right_x):
                buf[y, x] = snippet[idx]
                idx += 1

    img = Image.fromarray(buf)
    img.save("flag.jpeg")


if __name__ == '__main__':
    asyncio.run(main())
