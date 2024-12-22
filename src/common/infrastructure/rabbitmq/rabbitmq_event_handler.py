import pika

class RabbitMqQueuePublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def publish(self, name, event):
        self.channel.queue_declare(queue=name)
        self.channel.basic_publish(exchange='', routing_key=name, body=event)