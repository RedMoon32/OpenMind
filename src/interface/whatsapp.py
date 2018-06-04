from app.mac import mac, signals
from run import *
from interface.Messenger import Messenger

USER_ASKS_PATTERN = "{} {} asks: '{}'"
bot = None


class WhatsApp(Messenger):

    def __init__(self, language_model, app_dict, w2v, message_bundle, config):
        super().__init__(language_model, app_dict, w2v, message_bundle, config)
        global bot
        bot = self
        self.__step = 0

    def start(self):
        run()

    def stop(self):
        pass

    def process_request__(self, mess):
        request = mess.text.strip()
        if (request == ')' or request == '('):
            self.evaluate(mess)
            return
        user_id = int(mess.who.split('@')[0])
        user_name = mess.who_name
        answer = super().proccess_request(user_id, user_name, request)
        mac.send_message(answer.message, mess.conversation)

    def evaluate(self, mess):
        request = mess.text.strip()
        user_id = int(mess.who.split('@')[0])
        mark = 1 if request == ')' else 0
        ans = self.evaluate_(self.__step,user_id, mark)
        if ans != None:
            mac.send_message(ans, mess.conversation)
            self.__step += 1


@signals.message_received.connect
def handle(message):
    if (bot != None):
        bot.process_request__(message)
    else:
        pass
