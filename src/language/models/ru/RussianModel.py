from pycorenlp import StanfordCoreNLP
from configs.config_constants import CoreNLPServerAddress
from language.models.named_entity_recognition import NERType
from language.models.part_of_speech import POS
from language.models.token import Token
from language.models.language_model import LanguageModel
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


class RussianLanguageModel(LanguageModel):
    __name = "Russian"
    __code = "ru"

    def __init__(self, config):
        self.pos_map = {"VERB": POS.VERB,
                        "INFN": POS.VERB,
                        "NOUN": POS.NOUN,
                        "NPRO": POS.NOUN,
                        "ADJF": POS.ADJ,
                        "ADJS": POS.ADJ,
                        "NUMR": POS.CARDINAL_NUMBER,
                        "PRTF": POS.PARTICLE,
                        "PRTS": POS.PARTICLE,
                        }

        self.ner_map = {"Name": NERType.PERSON,
                        "Surn": NERType.PERSON,
                        "NUMB": NERType.NUMBER}

        self.__question_words = {"где", "кто", "что", "когда", "почему", "чей", "какой", "как"}

    def get_language_name(self):
        return RussianLanguageModel.__name

    @property
    def language_code(self):
        return RussianLanguageModel.__code

    def convert_pos(self, pos_str):
        return self.pos_map.get(pos_str, POS.UNKOWN)

    def convert_ner(self, ner):
        ner = ner.upper()
        return self.ner_map.get(ner, None)

    def is_question(self, tokens_list):
        lemma = tokens_list[0].get_lemma()
        return lemma in self.__question_words

    def tokenize(self, string):
        splited = string.split(' ')
        result = []
        for word in splited:
            description = morph.parse(word)[0]
            lemma = description.normal_form
            pos_tag = self.convert_pos(description.tag.POS)
            token = Token(word, lemma, pos_tag)
            result.append(token)
        return result

r=RussianLanguageModel(None)
a=r.tokenize('Привет 33 зовут Илья')
print()