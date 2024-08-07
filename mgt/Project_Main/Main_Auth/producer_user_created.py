import json,pika
ROUTING_KEY = 'user.created.key'
EXCHANGE = 'user_exchange'
THREAD = 5
class ProducerUserCreated:
    def __init__(self) -> None:
                # hearbeat = 600 indicates that after 600 seconds 
        # the peer TCP connection should be considered unreachable 
        #  by RabbitMQ and client libraries
        #
        #blocked_connection_timeout=300 means after 300 seconds 
        # the peer TCP connection is interrupted and dropped.
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost',heartbeat=600,blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()

    def publish(self,method,body):
        print("Inside UserService: Sending to RabbitMQ")
        print(body)
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(exchange=EXCHANGE,routing_key=ROUTING_KEY,body=json.dumps(body),properties=properties        )