from configparser import ConfigParser
from assistant.intent_detector import IntentDetector
from interface.console import Console
from interface.telegram import Telegram
from configs.config_constants import InterfaceTypeKey, LogLevelKey, \
    IsStubMode
from threading import Thread
import logging
import os
from Language_model_factory import load_language

STARTED_WORKING_MESSAGE = "Assistant started working"
TELEGRAM = "telegram"
CONSOLE = "console"


def start():
    print("Started initialization")
    config_path = "configs/config.ini"
    if not os.path.isfile(config_path):
        config_path = "configs/default_config.ini"
    config_parser = ConfigParser()
    config_parser.read(config_path, encoding="utf-8")
    default_config = config_parser["DEFAULT"]

    logging.basicConfig(level=default_config[LogLevelKey],
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.info("Stub mode: {}".format(default_config[IsStubMode]))
    language_model, message_bundle, app_dict, w2v = load_language("ru", default_config)
    print("Making assistant")

    detector: IntentDetector = IntentDetector(default_config, app_dict, w2v)

    interface_type = default_config[InterfaceTypeKey]
    interface_type = CONSOLE
    interface_class = get_interface(interface_type)
    interface = interface_class(language_model, detector, message_bundle, default_config)

    if interface_type == CONSOLE:
        print(STARTED_WORKING_MESSAGE)
        interface.start()
    elif interface_type == TELEGRAM:
        assistant_thread = Thread(target=interface, name="Assistant")
        assistant_thread.start()
        print(STARTED_WORKING_MESSAGE)

        request = input("User: ")
        while request != "exit":
            request = input("User: ")

    interface.stop()
    print("Assistant stopped working")


def get_interface(interface):
    clazz = None
    if interface == CONSOLE:
        clazz = Console
    elif interface == TELEGRAM:
        clazz = Telegram

    logging.info("Chosen {} mode".format(clazz.__name__))
    return clazz


if __name__ == "__main__":
    start()
