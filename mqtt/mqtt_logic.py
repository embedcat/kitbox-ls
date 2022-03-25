import enum
import paho.mqtt.publish as publish
from config import settings


MQTT_BROKER_AUTH = {"username": f"{settings.MQTT_BROKER_USERNAME}", "password": f"{settings.MQTT_BROKER_PASSWORD}"}


class MqttTopic(enum.Enum):
    event = "kitbox/event"
    cmd = "kitbox/cmd"


class MqttEvent(enum.Enum):
    none = 0
    info = 1
    error = 2
    sale = 3
    modem = 4


class MqttCmd(enum.Enum):
    publish_on = 1
    publish_off = 2
    logger_clear = 3
    logger_start = 4
    logger_stop = 5
    logger_send = 6


def get_mqtt_events_list() -> list:
    return [
        (MqttEvent.none.value, "Нет событий"),
        (MqttEvent.info.value, "Информация"),
        (MqttEvent.error.value, "Ошибка"),
        (MqttEvent.sale.value, "Продажа"),
        (MqttEvent.modem.value, "Модем"),
    ]


def get_mqtt_cmd_list() -> list:
    return [
        (MqttCmd.publish_on.value, "Включить публикацию событий"),
        (MqttCmd.publish_off.value, "Выключить публикацию событий"),
        (MqttCmd.logger_clear.value, "Логгер: очистка лога"),
        (MqttCmd.logger_start.value, "Логгер: начать запись логов"),
        (MqttCmd.logger_stop.value, "Логгер: остановить запись логов"),
        (MqttCmd.logger_send.value, "Логгер: получить логи на сервер"),
    ]


def get_mqtt_logger_modules_start() -> list:
    return [
        (),
    ]


def get_mqtt_event_name(event: int) -> str:
    for item in get_mqtt_events_list():
        if event == item[0]:
            return f"{item[1]} ({item[0]})"
    return ""


def mqtt_publish_cmd(modem_id: int, cmd: int) -> None:
    publish.single(topic=f"{MqttTopic.cmd.value}/{str(modem_id)}", payload=cmd,
                   hostname=settings.MQTT_BROKER_IP, port=int(settings.MQTT_BROKER_PORT), auth=MQTT_BROKER_AUTH)


