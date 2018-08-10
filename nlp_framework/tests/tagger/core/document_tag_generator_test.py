from unittest import TestCase
from hamcrest import contains_inanyorder, has_entries
from hamcrest.core import assert_that
from tagger.core import TagGenerator


class DocumentTagGeneratorTest(TestCase):
    topics_tokens_map = {
        "0": {"network": 0.02, "authentication": 0.3, "router": 0.4, "content": 0.1},
        "1": {"network": 0.2, "cable": 0.3, "ethernet": 0.3, "socket": 0.2},
        "2": {"python": 0.2, "java": 0.30, "clojure": 0.40, "golang": 0.1},
    }

    def test_should_get_tags_for_given_documents_topics_and_tokens(self):
        documents_tokens_map = {
            "sha1": ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication", "content",
                     "router", "wifi", "cable", "ethernet", "socket", "authentication"],
            "sha2": ["java", "golang", "python", "clojure", "socket"],
            "sha3": ["authentication", "golang", "socket", "clojure"],
            "sha4": ["network", "cable", "ethernet", "monitor", "reliability", "cable", "ethernet", "content",
                     "network",
                     "router", "wifi", "cable", "ethernet", "socket", "authentication"],
            "sha5": ["python", "python", "python", "java"]
        }
        documents_topics_map = {
            "sha1": [("0", 0.80), ("1", 0.1)],
            "sha2": [("2", 0.90), ("1", 0.1)],
            "sha3": [("2", 0.5), ("1", 0.5)],
            "sha4": [("0", 0.1), ("1", 0.9)],
            "sha5": [("2", 0.92)]
        }
        expected_documents_tags_hamcrest_assert = has_entries("sha1", contains_inanyorder("router", "authentication",
                                                                                          "content")), has_entries(
            "sha2", contains_inanyorder("java", "clojure", "python")), has_entries("sha3", contains_inanyorder(
            "clojure")), has_entries("sha4", contains_inanyorder("ethernet", "socket", "network")), has_entries("sha5",
                                                                                                                contains_inanyorder(
                                                                                                                    "python",
                                                                                                                    "java"))

        document_tag_generator = TagGenerator(self.topics_tokens_map)
        actual_documents_tags_map = document_tag_generator.generate_documents_tag_map(
            documents_tokens_map=documents_tokens_map, documents_topics_map=documents_topics_map, top_n=3)
        assert_that(actual_documents_tags_map, expected_documents_tags_hamcrest_assert)

    def test_should_get_tags_for_given_document_topics_and_tokens(self):
        tokens = ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication", "content",
                  "router", "wifi", "cable", "ethernet", "socket", "authentication"]
        topics = [("0", 0.80), ("1", 0.1)]
        tag_generator = TagGenerator(self.topics_tokens_map)
        tags = tag_generator.generate_tags(topics, tokens, top_n=3)
        expected_tags = ["router", "authentication", "content"]
        self.assertItemsEqual(tags, expected_tags)


