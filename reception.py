import random
from paho.mqtt import client as mqtt_client
import sqlite3
from datetime import datetime
import json

broker = 'broker.emqx.io'
port = 1883
topic = "/foo/MeXam/meteo/serignan"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# ---------- FONCTION INSERTION BDD ----------
def insert_db(weather_data):
    if weather_data is not None:
        db = sqlite3.connect("serignan.db")
        cursor = db.cursor()

        cursor.execute('''
            INSERT INTO meteo 
            (ville, pays, temp, ressenti, humidite, description, vent, date_heure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather_data.get("ville"),
            weather_data.get("pays"),
            weather_data.get("temp"),
            weather_data.get("ressenti"),
            weather_data.get("humidite"),
            weather_data.get("description"),
            weather_data.get("vent_m_s"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        db.commit()
        db.close()
        print("✅ Données enregistrées dans la base SQLite.")

# ---------- CONNEXION MQTT ----------
def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.enable_logger()
    client.on_connect = on_connect
    return client

# ---------- ABONNEMENT ----------
def subscribe(client: mqtt_client.Client):
    def on_message(client, userdata, msg):
        try:
            payload = msg.payload.decode("utf-8")
            print("📥 Message reçu :", payload)
            weather_data = json.loads(payload)
            insert_db(weather_data)
        except Exception as e:
            print("❌ Erreur traitement du message :", e)

    client.on_message = on_message

# ---------- MAIN ----------
def run():
    client = connect_mqtt()
    client.connect(broker, port)
    client.loop_start()
    while True :
        subscribe(client)


run()
