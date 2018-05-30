from typing import Dict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from assistant.answer import AssistantAnswer
from configs.config_constants import StartMessageKey, TokenKey, PrintMessages
from assistant.assistant import Assistant
from interface.base_interface import BaseInterface

USER_ASKS_PATTERN = "User {} {} asks: '{}'"
ASSISTANT_ANSWERS_PATTERN = "Answer for user {} {}: '{}'"
STOP_MESSAGE_KEY = "stop_message_key"


class Telegram(BaseInterface):

    def __init__(self, language_model, app_dict, w2v, message_bundle, config):
        super().__init__(message_bundle, config)

        self.__language_model = language_model
        self.__app_dict = app_dict
        self.__w2v = w2v
        self.__token = self.config[TokenKey]
        self.__START_MESSAGE_KEY = self.config[StartMessageKey]
        self.__user_assistant_dict: Dict[int, Assistant] = {}

        self.__updater = Updater(self.__token)
        dp = self.__updater.dispatcher
        dp.add_handler(CommandHandler("start", self.slash_start), group=0)
        dp.add_handler(CommandHandler("stop", self.slash_stop), group=0)
        dp.add_handler(CallbackQueryHandler(self.evaluate))
        dp.add_handler(MessageHandler(Filters.text, self.idle_main))

    def idle_main(self, bot, update):
        request = update.message.text.strip()
        user_id = update.message.chat_id
        does_print = bool(self.config[PrintMessages])
        user_name = update.message.from_user.username
        if does_print:
            print((USER_ASKS_PATTERN.format(user_id, user_name, request)))
        assistant: Assistant = self.__user_assistant_dict.get(user_id, None)
        if assistant is None:
            assistant: Assistant = Assistant(self.__language_model, self.message_bundle, self.__app_dict,
                                             self.config, w2v=self.__w2v, user_id=user_id)
            self.__user_assistant_dict[user_id] = assistant
        answer = assistant.process_request(request)
        message = answer.message
        if does_print:
            print(ASSISTANT_ANSWERS_PATTERN.format(user_id, user_name, message))

        buttons = self.get_buttons(answer.dialog_step)
        bot.sendMessage(user_id, text=message, reply_markup=buttons)
        if answer.picture is not None:
            image = answer.picture
            if hasattr(image, 'read'):
                bot.sendPhoto(user_id, photo=image)

    def slash_start(self, bot, update):
        bot.sendMessage(update.message.chat_id, text=self.message_bundle[self.__START_MESSAGE_KEY])

    def slash_stop(self, bot, update):
        user_id: int = update.message.chat_id
        assistant: Assistant = self.__user_assistant_dict.get(user_id, None)
        if assistant is not None:
            assistant.stop()
            del self.__user_assistant_dict[user_id]
            bot.sendMessage(update.message.chat_id, text=self.message_bundle[STOP_MESSAGE_KEY])

    def evaluate(self, bot: Bot, update):
        query = update.callback_query
        user_id = query.message.chat_id
        raw_data = query.data
        data_list = raw_data.split("_")
        mark = data_list[0]
        dialog_step = int(data_list[1])
        assistant: Assistant = self.__user_assistant_dict.get(user_id)
        if assistant:
            answer: AssistantAnswer = assistant.mark(dialog_step, mark)
            if answer:
                bot.sendMessage(user_id, text=answer.message)

    def start(self):
        self.__updater.start_polling()

    def stop(self):
        self.__updater.stop()
        for assistant in self.__user_assistant_dict.values():
            assistant.stop()

    def get_buttons(self, message_id) -> InlineKeyboardMarkup:
        button_list = [[
            InlineKeyboardButton("👎", callback_data="0_{}".format(message_id)),
            InlineKeyboardButton("👍", callback_data="1_{}".format(message_id))
        ]]
        buttons = InlineKeyboardMarkup(button_list)
        return buttons
