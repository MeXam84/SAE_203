import requests
import json
from paho.mqtt import client as mqtt_client

# -------- PARAMÈTRES --------
mqtt_broker = "broker.emqx.io"  # Remplacez par l'adresse de votre broker
mqtt_port = 1883
mqtt_topic = "/foo/MeXam/meteo/serignan"
payload = {"Led" : "On"}
json_payload = json.dumps(payload)


# -------- PUBLICATION MQTT --------
def publish_mqtt(broker, port, topic, payload):
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    try:
        client.connect(broker, port, 60)
        client.publish(topic, payload)
        print(f"Données publiées sur MQTT : {topic}")
    except Exception as e:
        print(f"Erreur MQTT : {e}")
    finally:
        client.disconnect()

# -------- MAIN --------
publish_mqtt(mqtt_broker, mqtt_port, mqtt_topic, json_payload)
