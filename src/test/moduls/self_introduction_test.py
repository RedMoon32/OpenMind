import unittest

from constants import FORM_ACTION_NAME
from language.models.message_constant import INTRODUCTION_MESSAGE, HI_MESSAGE
from moduls.self_introduction import SelfIntroductionModule


class SelfIntroductionModuleTest(unittest.TestCase):

    def setUp(self):
        self.module = SelfIntroductionModule(None)

    def test_1(self):
        parameters_dict = {FORM_ACTION_NAME: "Ability demonstration"}
        answer = self.module.run(None, parameters_dict)
        self.assertEqual(INTRODUCTION_MESSAGE, answer.message_key)
        self.assertIsNone(answer.parameters)

    def test_2(self):
        parameters_dict = {FORM_ACTION_NAME: "Say hi"}
        answer = self.module.run(None, parameters_dict)
        self.assertEqual(HI_MESSAGE, answer.message_key)
        self.assertIsNone(answer.parameters)

    def test_3(self):
        parameters_dict = {FORM_ACTION_NAME: "Say goodbye"}
        answer = self.module.run(None, parameters_dict)
        self.assertEqual(HI_MESSAGE, answer.message_key)
        self.assertIsNone(answer.parameters)