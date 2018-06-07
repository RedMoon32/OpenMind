from app.mac import mac, signals
from run import *
from modules.PDA_Bot.Pda import set_bot
from interface.Messenger import *
from threading import Thread
from time import sleep
USER_ASKS_PATTERN = "{} {} asks: '{}'"


class WhatsApp(Messenger):

    def __init__(self, language_model, app_dict, w2v, message_bundle, config):
        super().__init__(language_model, app_dict, w2v, message_bundle, config)
        self.__step = 0

    def start(self):
        t=Thread(target=run,args=())
        t.start()
        set_bot(self)

    def stop(self):
        pass

    def process_request__(self, mess):
        request = mess.text.strip()
        if (request == '👍' or request == '👎'):
            self.evaluate(mess)
        else:
            user_id = int(mess.who.split('@')[0])
            user_name = mess.who_name
            answer = super().proccess_request(user_id, user_name, request)
            mac.send_message(answer.message, mess.conversation)

    def evaluate(self, mess):
        request = mess.text.strip()
        user_id = int(mess.who.split('@')[0])
        mark = 1 if request == '👍' else 0
        ans = self.evaluate_request(self.__step, user_id, mark)
        if ans != None:
            mac.send_message(ans, mess.conversation)
            self.__step += 1
