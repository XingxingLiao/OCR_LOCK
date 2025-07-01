# import paho.mqtt.client as mqtt
# import json
# from config import mqtt_broker, mqtt_port, mqtt_topic

# def send_mqtt_message(message):
#     client = mqtt.Client()
#     client.connect(mqtt_broker, mqtt_port, 60)
#     client.publish(mqtt_topic, json.dumps(message))
#     client.disconnect()
# mqtt_sender.py

import paho.mqtt.client as mqtt
import ssl
import json
from config import mqtt_broker, mqtt_port, mqtt_topic, mqtt_username, mqtt_password

def send_message(payload):
    client = mqtt.Client()

    client.tls_set(tls_version=ssl.PROTOCOL_TLS)


    client.username_pw_set(mqtt_username, mqtt_password)

    # 连接并发布
    try:
        client.connect(mqtt_broker, mqtt_port)
        client.loop_start()
        client.publish(mqtt_topic, payload)
        client.loop_stop()
        client.disconnect()
        print(f"succeed in sending {mqtt_topic}: {payload}")
    except Exception as e:
        print(f"fail to send data: {e}")
