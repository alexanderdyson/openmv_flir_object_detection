'''
    mqtt_publisher.py
'''
import time
import network
import json
from mqtt import MQTTClient


class AWSIOTCoreMQTTClient:
    def __init__(self, network_ssid, network_key, key_path, cert_path,
                 client_id, mqtt_endpoint):
        self.client_id = client_id
        self.network_ssid = network_ssid
        self.network_key = network_key
        self.key_path = key_path
        self.cert_path = cert_path
        self.mqtt_endpoint = mqtt_endpoint
        self.wlan = None

        self.connect_wlan()

        key, cert = self.read_keys()

        ssl_params = {"key": key, "cert": cert, "server_side": False}

        self.mqtt_client = MQTTClient(client_id=client_id, server=mqtt_endpoint,
                                      keepalive=0, ssl=True,
                                      ssl_params=ssl_params)

        self.mqtt_client.connect()

    def connect_wlan(self):
        self.wlan = network.WINC()

        self.wlan.connect(self.network_ssid, key=self.network_key,
                          security=self.wlan.WPA_PSK)

        if not self.wlan.isconnected():
            raise Exception("Unable to connect to network")

        print("Connected to network")

    def read_keys(self):
        key, cert = None, None

        with open(self.key_path, 'r') as f:
            key = f.read()
        with open(self.cert_path, 'r') as f:
            cert = f.read()

        return key, cert

    def publish(self, topic, data):
        try:
            print("Sending topic and data ", topic, data)
            self.mqtt_client.publish(topic, data)
        except Exception as e:
            print("Error in MQTT publish", e)
