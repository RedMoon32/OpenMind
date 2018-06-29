from configparser import ConfigParser
from application.application_config import load_config
from language.models.ru.RussianModel import RussianLanguageModel
from language.models.en.english_language_model import EnglishLanguageModel
from configs.config_constants import RusW2VModelFileTypeKey, RusW2VModelPathKey, InterfaceTypeKey, LogLevelKey, \
    IsStubMode, W2VModelPathKey, W2VModelFileTypeKey
from gensim.models.keyedvectors import KeyedVectors
from distutils.util import strtobool
import logging

language_model_map = {
    "ru":
        {
            "model": RussianLanguageModel,
            "is_binary": RusW2VModelFileTypeKey,
            "W2Vpath": RusW2VModelPathKey,
            "message_bundle": "language/models/ru/message.ini",
            "app_config": "RussianApplicationConfig.json"
        },
    "en":
        {
            "model": EnglishLanguageModel,
            "is_binary": W2VModelFileTypeKey,
            "W2Vpath": W2VModelPathKey,
            "message_bundle": "language/models/en/message.ini",
            "app_config": "ApplicationConfig.json"
        }
}


def load_language(language_code, default_config):
    language = language_model_map[language_code]
    language_model = language["model"](default_config)
    logging.info("Selected {} language mode".format(language_model.get_language_name()))

    config_parser = ConfigParser()
    config_parser.read(language["message_bundle"], encoding="utf-8")
    message_bundle = config_parser["DEFAULT"]
    app_dict = load_config(language["app_config"], language_model)

    print("Started initialization of Word2Vect")
    is_binary_w2v = strtobool(default_config[language["is_binary"]])
    w2v = KeyedVectors.load_word2vec_format(default_config[language["W2Vpath"]], binary=is_binary_w2v)
    return language_model, message_bundle, app_dict, w2v
