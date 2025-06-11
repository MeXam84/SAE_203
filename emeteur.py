import requests
import json
from paho.mqtt import client as mqtt_client

# -------- PARAMÈTRES --------
api_key = "3d6a425d39070584b5c66110fd2848cc"
ville = "Serignan-du-Comtat"
mqtt_broker = "broker.emqx.io"  # Remplacez par l'adresse de votre broker
mqtt_port = 1883
mqtt_topic = "/foo/MeXam/meteo/serignan"

# -------- RÉCUPÉRATION MÉTÉO --------
def get_weather(city_name, api_key):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric',
        'lang': 'fr'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "ville": data['name'],
            "pays": data['sys']['country'],
            "temp": data['main']['temp'],
            "ressenti": data['main']['feels_like'],
            "humidite": data['main']['humidity'],
            "description": data['weather'][0]['description'],
            "vent_m_s": data['wind']['speed']
        }
        return weather_data
    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None

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
weather = get_weather(ville, api_key)
if weather:
    json_payload = json.dumps(weather, ensure_ascii=False)
    print(f"Données météo récupérées : {json_payload}")
    publish_mqtt(mqtt_broker, mqtt_port, mqtt_topic, json_payload)
