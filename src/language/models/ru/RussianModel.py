from pycorenlp import StanfordCoreNLP
from configs.config_constants import CoreNLPServerAddress
from language.models.named_entity_recognition import NERType
from language.models.part_of_speech import POS
from language.models.token import Token
from language.models.language_model import LanguageModel
import pymorphy2
import re

morph = pymorphy2.MorphAnalyzer()


class RussianLanguageModel(LanguageModel):
    __name = "Russian"
    __code = "ru"

    def __init__(self, config=None):
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

        self.pymorph_to_w2v_map = {"VERB": "VERB",
                                   "INFN": "VERB",
                                   "ADJF": "ADJ",
                                   "ADJS": "ADJ",
                                   "NOUN": "NOUN",
                                   "ADVB": "ADV",
                                   "NUMR": "NUM",
                                   "PRTF": "PART",
                                   "PRTS": "PART",
                                   "NPRO": "NOUN",
                                   "PNCT": "PUNCT"
                                   }

    def get_language_name(self):
        return RussianLanguageModel.__name

    @property
    def language_code(self):
        return RussianLanguageModel.__code

    def convert_pos(self, pos_str):
        return self.pos_map.get(pos_str, POS.UNKOWN)

    def pos_from_pymorph_to_w2v(self, str):
        return self.pymorph_to_w2v_map.get(str, "unkown")

    def convert_ner(self, ner):
        raise NotImplementedError()

    def get_w2v_form(self, lemma, pos):
        return lemma + '_' + self.pos_from_pymorph_to_w2v(pos)

    def tokenize(self, string):
        splited = string.split(' ')
        result = []
        for word in splited:
            word = "".join([c for c in word if c not in ['?', '!', '_']])
            description = morph.parse(word)[0]
            lemma = description.normal_form
            pos_tag = self.convert_pos(description.tag.POS)
            vect_form = lemma
            if description.tag.POS != None:
                vect_form = self.get_w2v_form(lemma, description.tag.POS)
            token = Token(word, lemma, pos_tag, vect_form)
            result.append(token)
        return result
