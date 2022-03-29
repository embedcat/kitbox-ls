import enum
import paho.mqtt.publish as publish
from config import settings


MQTT_BROKER_AUTH = {"username": f"{settings.MQTT_BROKER_USERNAME}", "password": f"{settings.MQTT_BROKER_PASSWORD}"}


class MqttTopic(enum.Enum):
    event = "event"
    cmd = "cmd"


class MqttEvent(enum.Enum):
    none = 0
    info = 1
    error = 2
    sale = 3
    modem = 4


class MqttCmd(enum.Enum):
    publish_filter = 1
    logger_clear = 2
    logger_start = 3
    logger_stop = 4
    logger_send = 5


class MqttLoggerModules(enum.Enum):
    bus1 = 1
    bus2 = 2


def get_mqtt_events_list() -> list:
    return [
        (MqttEvent.info.value, "Информация"),
        (MqttEvent.error.value, "Ошибка"),
        (MqttEvent.sale.value, "Продажа"),
        (MqttEvent.modem.value, "Модем"),
    ]


def get_mqtt_cmd_list() -> list:
    return [
        (MqttCmd.publish_filter.value, "Включить публикацию событий"),
        (MqttCmd.logger_clear.value, "Логгер: очистка лога"),
        (MqttCmd.logger_start.value, "Логгер: начать запись логов"),
        (MqttCmd.logger_stop.value, "Логгер: остановить запись логов"),
        (MqttCmd.logger_send.value, "Логгер: получить логи на сервер"),
    ]


def get_mqtt_logger_modules_start() -> list:
    return [
        (MqttLoggerModules.bus1.value, "Шина-1"),
        (MqttLoggerModules.bus2.value, "Шина-2"),
    ]


def get_mqtt_publish_filter_list() -> list:
    return get_mqtt_events_list()


def get_mqtt_event_name(event: int) -> str:
    for item in get_mqtt_events_list():
        if event == item[0]:
            return f"{item[1]} ({item[0]})"
    return ""


def mqtt_publish_cmd(modem_id: int, cmd: int, payload: str) -> None:
    publish.single(topic=f"{MqttTopic.cmd.value}/{str(modem_id)}/{str(cmd)}", payload=payload,
                   hostname=settings.MQTT_BROKER_IP, port=int(settings.MQTT_BROKER_PORT), auth=MQTT_BROKER_AUTH)


