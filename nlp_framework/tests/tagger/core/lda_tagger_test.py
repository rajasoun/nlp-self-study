import os
import threading
import unittest

from mock import Mock, call
from tagger.core import LDATagger
from trinity import Logger

logger = Logger.get_logger("LDATaggerTest")


class LDATaggerTest(unittest.TestCase):
    def setUp(self):
        self.test_model_path = os.path.join(os.path.dirname(__file__), "../model")
        self.tokens_list = {
            "1": ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication", "content",
                  "network", "router", "wifi", "cable", "ethernet", "socket", "authentication"],
            "2": ["java", "golang", "cool", "awesome"],
            "3": ["authentication", "golang", "impossible"],
            "4": ["network", "tcp", "ftp", "monitor", "reliability", "cable", "ethernet", "content", "network",
                  "router",
                  "wifi", "cable", "ethernet", "socket", "authentication"],
            "5": ["python", "topic", "modelling", "module"]
        }

    def tearDown(self):
        model_file = os.path.join(self.test_model_path, "lda.model")
        dict_file = os.path.join(self.test_model_path, "tokens.dict")
        if os.path.exists(model_file):
            os.remove(model_file)
        if os.path.exists(dict_file):
            os.remove(dict_file)

    def build_save_model(self):
        tagger = LDATagger(self.test_model_path)
        tagger.build_topics(self.tokens_list.values())
        return tagger

    def test_shouldBuildAndSaveTopicModel(self):
        model_file = os.path.join(self.test_model_path, "lda.model")
        dict_file = os.path.join(self.test_model_path, "tokens.dict")
        self.build_save_model()
        self.assertTrue(os.path.exists(model_file))
        self.assertTrue(os.path.exists(dict_file))

    def test_shouldGetTopicsGivenTokensList(self):
        number_of_docs = len(self.tokens_list)
        tagger = self.build_save_model()
        topics = tagger.topics_for_documents(self.tokens_list)
        for id, topic in enumerate(topics):
            logger.info("Document %d: %s" % (id, str(topic)))

        self.assertEquals(number_of_docs, len(topics))

    def test_shouldInferTopicsFromExistingModelGivenNewDocument(self):
        tokens = ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication", "content",
                  "network", "router", "wifi", "cable", "ethernet", "socket", "authentication"]
        tagger = self.build_save_model()
        topics = tagger.topics_for_document(tokens)
        logger.info("Topics: %s" % str(topics))
        self.assertTrue(topics)

    def test_shouldGetTopicsToTokensAssociation(self):
        tagger = self.build_save_model()
        tokens_to_topics = tagger.topics_to_tokens()

        self.assertTrue(tokens_to_topics != None)

    def test_shouldDemonstrateLockingOnSaveModelMethod(self):
        from concurrent.futures import ThreadPoolExecutor

        number_of_threads = 10
        synchronised_block_recorder = Mock(wraps=threading.Lock())

        tagger = LDATagger(self.test_model_path, lock=threading.Lock())
        tagger.build_topics(self.tokens_list.values())

        expected_ordered_calls = []
        with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
            for i in range(number_of_threads):
                executor.submit(tagger.save_model, True, synchronised_block_recorder)
                expected_ordered_calls.append(call.acquire())
                expected_ordered_calls.append(call.release())

        self.assertTrue(len(synchronised_block_recorder.mock_calls) == (number_of_threads * 2))
        self.assertEquals(synchronised_block_recorder.mock_calls, expected_ordered_calls)


if __name__ == '__main__':
    unittest.main()
