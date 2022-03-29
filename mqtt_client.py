import json
import logging
import os
import random
import paho.mqtt.client as mqtt_client
from datetime import datetime
from config import settings
from config import setup

setup()

from logserver.models import MQTTDevice, Event
from mqtt.mqtt_logic import MqttTopic

SUBSCRIBE_FILE = "mqtt/subscribe.json"
EVENTS_FILE = "mqtt/events.json"
LOGGING_FILE = "log_mqtt_client.log"

logger = logging.getLogger("MQTTClientLogger")

client = mqtt_client.Client()


def _store_message_db(message: mqtt_client.MQTTMessage):
    modem_id = int(message.topic.split("/")[1])
    try:
        device = MQTTDevice.objects.get(modem_id=modem_id)
    except (MQTTDevice.DoesNotExist, TypeError):
        logger.error(f"Msg don't stored, because Device with modem_id={modem_id} not found in DB")
        return
    type = str(message.topic.split("/")[2])
    event = Event.objects.create(
        device=device,
        type=type,
        payload=message.payload.decode("utf-8")
    )


def _on_connect(client, userdata, flags, rc):
    logger.info("Connected")
    client.subscribe(f"{MqttTopic.event.value}/#")


def _on_disconnect(client, userdata, rc):
    logger.info("Disconnected")


def _on_message(client, userdata, message):
    # print(f"Received: \"{message.topic}\" : \"{message.payload}\"")
    logger.info(f"Msg received. Topic: <{message.topic}>. Msg: <{message.payload.decode('utf-8')}>")
    _store_message_db(message=message)


def _on_publish(client, userdata, message):
    logger.info(f"Msg published. Topic: <{message.topic}>. Msg: <{message.payload.decode('utf-8')}>")


def _on_subscribe(client, userdata, mid, granted_qos):
    logger.info(f"Subscribed")


def main():
    logger.info("MQTT Client script started")

    client.username_pw_set(settings.MQTT_BROKER_USERNAME, settings.MQTT_BROKER_PASSWORD)
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.on_publish = _on_publish
    client.on_disconnect = _on_disconnect
    client.on_subscribe = _on_subscribe

    client.connect(host=settings.MQTT_BROKER_IP, port=int(settings.MQTT_BROKER_PORT))
    client.loop_forever()
    # client.connect_async(host=MQTT_BROKER_IP, port=int(MQTT_BROKER_PORT))
    # client.loop_start()


if __name__ == "__main__":
    main()
