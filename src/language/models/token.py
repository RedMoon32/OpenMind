class Token:
    def __init__(self, word, lemma, pos_tag, w2v_form=None):
        self.word = word
        self.lemma = lemma
        self.pos_tag = pos_tag
        self.ner_type = None
        self.ner_value = None
        self.w2v_form = lemma.lower() if w2v_form == None else w2v_form

    def get_lemma(self):
        return self.lemma

    def get_word(self):
        return self.word

    def get_pos(self):
        return self.pos_tag

    def set_NER_type(self, ner_type):
        self.ner_type = ner_type

    def set_NER_value(self, value):
        self.ner_value = value

    def get_NER_type(self):
        return self.ner_type

    def get_NER_value(self):
        return self.ner_value

    def get_w2v_form(self):
        return self.w2v_form
