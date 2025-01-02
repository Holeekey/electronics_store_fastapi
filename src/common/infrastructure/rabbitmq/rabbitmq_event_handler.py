import json
import threading
import pika
import jsonpickle

from common.application.events.event_handlers import IEventHandler, IEventListener, IEventPublisher
from common.domain.events.domain_event import DomainEvent
from config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME

class EventBind():
    def __init__(self, name: str, handler):
        self.name = name
        self.handler = handler

class RabbitMqEventHandler(IEventHandler):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
            )
        )
        self.channel = self.connection.channel()

    def setup_bindings(self, bindings: list[EventBind]):
        for binding in bindings:
            self.subscribe(binding.name, binding.handler)

    def close(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
            
    def start_consuming(self):
        self.channel.start_consuming()
        
    def start_consuming_in_thread(self):
        thread = threading.Thread(target=self.start_consuming)
        thread.start()


    async def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            self.channel.queue_declare(queue=event.name)
            self.channel.queue_declare(queue=event.name)
            event_data = jsonpickle.encode(event)
            self.channel.basic_publish(exchange='', routing_key=event.name, body=event_data)
            
    def subscribe(self, name, handler):
        self.channel.queue_declare(queue=name)
        self.channel.basic_consume(queue=name, on_message_callback=handler, auto_ack=True)
            

class RabbitMqEventListener(IEventListener):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
            )
        )
        self.channel = self.connection.channel()
        
    def close(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
        
    def setup_bindings(self, bindings: list[EventBind]):
        for binding in bindings:
            self.subscribe(binding.name, binding.handler)
        
    def start_consuming(self):
        self.channel.start_consuming()
        
    def start_consuming_in_thread(self):
        thread = threading.Thread(target=self.start_consuming)
        thread.start()
        
    def subscribe(self, name, handler):
        self.channel.queue_declare(queue=name)
        self.channel.basic_consume(queue=name, on_message_callback=handler, auto_ack=True)
    
class RabbitMqEventPublisher(IEventPublisher):
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, password=RABBITMQ_PASSWORD)
            )
        )
        self.channel = self.connection.channel()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
        
    async def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            event_data = jsonpickle.encode(event)
            self.channel.basic_publish(exchange='', routing_key=event.name, body=event_data)

            
rabbit_event_listener = RabbitMqEventListener()

async def get_rabbit_mq_event_publisher():
    with RabbitMqEventPublisher() as publisher:
        yield publisher