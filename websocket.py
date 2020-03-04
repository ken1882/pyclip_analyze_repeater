import asyncio
import websockets
from threading import Thread

FPS = 1 / 120
FlagStop = False

class WebSocket:
  
  def __init__(self, port, domain="0.0.0.0"):
    self.flag_stop = False
    self.thread    = None
    self.handler   = {}
    self.instance  = websockets.serve(self.listen, domain, port)

  def start(self):
    asyncio.get_event_loop().run_until_complete(self.instance)
    loop = asyncio.get_event_loop()
    self.thread = Thread(target=self.main_loop, args=(loop,))
    self.thread.start()

  async def listen(self, ws, path):
    msg = await ws.recv()
    for f in self.handler.values():
      ret = f(msg)
      if ret:
        await ws.send(ret)

  @asyncio.coroutine
  def update(self):
    while not self.flag_stop:
      yield

  def main_loop(self, loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(self.update())

  def stop(self):
    self.flag_stop = True
  
  def add_handler(self, key, func):
    self.handler[key] = func

def test_handler(msg):
  print("Recived {}".format(msg))
  feedback = "OK " + msg
  print("Sent {}".format(feedback))
  return feedback

sk = WebSocket(5555, "localhost")
sk.add_handler("test", test_handler)
try:
  sk.start()
  while True:
    pass
finally:
  sk.stop()
