from assistant.intent_detector import IntentDetector
import unittest
from unittest.mock import Mock
from configs.config_constants import WMDThresholdKey


class IntentDetectorTest(unittest.TestCase):

    def setUp(self):
        self.config = {WMDThresholdKey: 2}

        samples = [["word"]]
        intent = Mock()
        intent.get_samples = Mock(return_value=samples)
        intent.get_name = Mock(return_value="my_intent_name")
        intents = [intent]
        mock_app = Mock()
        mock_app.get_intents_list = Mock(return_value=intents)
        mock_app.get_intents = Mock(return_value=dict())
        mock_app.get_name = Mock(return_value="my_name")

        self.application_dict = {"MockApp": mock_app}
        self.w2v = Mock()
        self.w2v.wmdistance = Mock(return_value=1)

        self.request = Mock()
        self.request.get_app_name = Mock(return_value=None)
        token = Mock(get_lemma=Mock(return_value="test_lemma"))
        tokens = [token]
        self.request.get_tokens_list = Mock(return_value=tokens)

    def test_1(self):
        detector = IntentDetector(self.config, self.application_dict, self.w2v)
        app, intent_description = detector.detect_intent(self.request)
        self.assertEqual(app.get_name(), "my_name")
        self.assertEqual(intent_description.get_name(), "my_intent_name")

    def test_2(self):
        config = {WMDThresholdKey: 0.5}
        detector = IntentDetector(config, self.application_dict, self.w2v)
        app, intent_description = detector.detect_intent(self.request)

        self.assertIsNone(app)
        self.assertIsNone(intent_description)
