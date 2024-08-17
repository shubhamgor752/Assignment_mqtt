import pika
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.mqtt_database
collection = db.messages

def callback(ch, method, properties, body):
    message = json.loads(body)
    collection.insert_one(message)it bra
    print(f"Stored in MongoDB: {message}")

def start_server():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare the same queue
    channel.queue_declare(queue='mqtt_queue')

    # Subscribe to the queue
    channel.basic_consume(queue='mqtt_queue', on_message_callback=callback, auto_ack=True)
    
    print("Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_server()
