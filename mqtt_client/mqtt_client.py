import pika
import json
import random
import time

def emit_mqtt_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare a queue for MQTT messages
    channel.queue_declare(queue='mqtt_queue')

    while True:
        status = random.randint(0, 6)
        message = {"status": status, "timestamp": time.time()}
        channel.basic_publish(exchange='', routing_key='mqtt_queue', body=json.dumps(message))
        print(f"Sent: {message}")
        time.sleep(1)

if __name__ == "__main__":
    emit_mqtt_messages()
