import paho.mqtt.client as mqtt
import json
from config import mqtt_broker, mqtt_port, mqtt_topic

def send_mqtt_message(message):
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    client.publish(mqtt_topic, json.dumps(message))
    client.disconnect()
