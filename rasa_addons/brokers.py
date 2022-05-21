from rasa.core.brokers.broker import EventBroker
from rasa.utils.endpoints import EndpointConfig
from typing import Optional, Dict, Text, Any
from asyncio import AbstractEventLoop
import json
import logging
from logging.handlers import RotatingFileHandler
import os


def init_logger(name: str, path: str, max_bytes: int, nb_file: int):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=nb_file)
    logger.addHandler(handler)
    return logger


class LoggerEventBroker(EventBroker):
    def __init__(self, config: Dict) -> None:
        os.makedirs(
            os.path.dirname(config.get("path", "./logs/rasa.log")), exist_ok=True
        )
        self.logger = init_logger(
            config.get("name", "rasa"),
            config.get("path", "./logs/rasa.log"),
            config.get("max_bytes", 1024 * 1024),
            config.get("nb_file", 10),
        )

    @classmethod
    async def from_endpoint_config(
        cls,
        broker_config: EndpointConfig,
        event_loop: Optional[AbstractEventLoop] = None,
    ) -> "EventBroker":
        return cls(broker_config.kwargs)

    def publish(self, event: Dict[Text, Any]) -> None:
        self.logger.debug(json.dumps(event))
        return None


if __name__ == "__main__":
    broker = LoggerEventBroker({"name": "rasa", "path": "./log/rasa.log"})
    broker.publish({})
