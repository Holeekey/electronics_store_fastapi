import json
import pika
import jsonpickle

from common.application.events.event_handlers import IEventPublisher
from common.domain.events.domain_event import DomainEvent
from config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USERNAME

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

    def publish(self, events: list[DomainEvent]) -> None:
        for event in events:
            self.channel.queue_declare(queue=event.name)
            event_data = jsonpickle.encode(event)
            self.channel.basic_publish(exchange='', routing_key=event.name, body=event_data)
        
        
async def get_rabbitmq_event_publisher():
    with RabbitMqEventPublisher() as publisher:
        yield publisher