from answer import AssistantAnswer
import random


class MatchesGameModule:

    def __init__(self):
        self.amount_of_matches = 0
        self.is_started = False

    def run(self, assistant, parameters_dict):
        intent = parameters_dict["Intent"]
        answer = None
        if intent == "Start Matches Game":
            answer = self.start(assistant, parameters_dict)
        elif intent == "User turn":
            answer = self.turn(assistant, parameters_dict)
        return answer


    def start(self, assistant, parameters_dict):
        self.amount_of_matches = 30
        self.is_started = True
        return AssistantAnswer("matches_game.start_game", {"matches": self.amount_of_matches})

    def turn(self, assistant, parameters_dict):
        answer = None
        if self.is_started:
            amount_to_remove = int(parameters_dict["Amount"])
            if 1 <= amount_to_remove <= 3:
                self.amount_of_matches -= amount_to_remove
                bot_choice = random.randint(1, 3)
                if self.amount_of_matches < 2:
                    answer = AssistantAnswer("matches_game.win")
                    self.is_started = False
                else:
                    self.amount_of_matches -= bot_choice
                    if self.amount_of_matches < 2:
                        answer = AssistantAnswer("matches_game.lose")
                        self.is_started = False
                    else:
                        params = {"matches": self.amount_of_matches,
                                  "amount": bot_choice}
                        answer = AssistantAnswer("matches_game.amount_of_matches", params)
            else:
                answer = AssistantAnswer("matches_game.wrong_input_amount")

        return answer