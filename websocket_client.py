import asyncio
import websockets

URI = "ws://localhost:5555"

async def handshake():
  async with websockets.connect(URI) as ws:
    msg = "Test Message"
    await ws.send(msg)
    print("Sent {}".format(msg))
    feedback = await ws.recv()
    print("Received {}".format(feedback))

asyncio.get_event_loop().run_until_complete(handshake())