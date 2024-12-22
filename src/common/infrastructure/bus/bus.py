from time import sleep
from typing import Callable
import uuid
from pydantic import BaseModel

class QueueItem(BaseModel):
    id: str
    data: object
    
class Bus:
    def __init__(self):
        self.bindings = {}
        self.queue = []

    async def dispatch(self, object: object):
        object_class_name = object.__class__.__name__
        if object_class_name in self.bindings:
            id = str(uuid.uuid4())
            event_item = QueueItem(id=id, data=object)
            self.queue.append(event_item)
            while self.queue[0].id != id:
                await sleep(0.00001)
            handler = self.bindings[object_class_name]
            result = await handler(object)
            self.queue.pop(0)
            return result

    def bind(self, type: type, handler):
        self.bindings[type.__name__] = handler

command_bus = Bus()

class Bind:
    def __init__(self, type: type, handler: Callable[[object], None]):
        self.type = type
        self.handler = handler

def setup_bindings(bus: Bus,bindings: list[Bind]):
    for binding in bindings:
        bus.bind(binding.type, binding.handler)

def get_command_bus():
    try:
        yield command_bus
    finally:
        pass
