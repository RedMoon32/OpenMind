from typing import Dict
from answer import AssistantAnswer
from configs.config_constants import StartMessageKey, TokenKey, PrintMessages
from assistant import Assistant
from interface.base_interface import BaseInterface

USER_ASKS_PATTERN = "User {} {} asks: '{}'"
ASSISTANT_ANSWERS_PATTERN = "Answer for user {} {}: '{}'"
STOP_MESSAGE_KEY = "stop_message_key"


class Messenger(BaseInterface):

    def __init__(self, language_model, app_dict, w2v, message_bundle, config):
        super().__init__(message_bundle, config)

        self.__language_model = language_model
        self.__app_dict = app_dict
        self.__w2v = w2v
        self.__token = self.config[TokenKey]
        self.__START_MESSAGE_KEY = self.config[StartMessageKey]
        self.user_assistant_dict: Dict[int, Assistant] = {}

    def proccess_request(self, user_id, user_name, request):
        does_print = bool(self.config[PrintMessages])
        if does_print:
            print((USER_ASKS_PATTERN.format(user_id, user_name, request)))
        assistant: Assistant = self.user_assistant_dict.get(user_id, None)
        if assistant is None:
            assistant: Assistant = Assistant(self.__language_model, self.message_bundle, self.__app_dict,
                                             self.config, w2v=self.__w2v, user_id=user_id)
            self.user_assistant_dict[user_id] = assistant
        answer = assistant.process_request(request)
        message = answer.message
        if does_print:
            print(ASSISTANT_ANSWERS_PATTERN.format(user_id, user_name, message))
        return answer

    def evaluate_(self,step,user_id,mark):
        assistant: Assistant = self.user_assistant_dict.get(user_id)
        if assistant:
            answer: AssistantAnswer = assistant.mark(step,mark)
            if answer:
                return answer.message
        return None
