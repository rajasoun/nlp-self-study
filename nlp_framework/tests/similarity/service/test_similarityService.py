from unittest import TestCase
from similarity.service import SimilarityService
from trinity import Logger

logger = Logger.get_logger("TestSimilarityService")


class TestSimilarityService(TestCase):
    def test_shouldFindSimilarity(self):
        input_documents = {
            "sha1": {
                "title": "this is a title",
                "body": "this is my first blog, hence sucks",
                "tags": []
            },

            "sha2": {
                "title": "this is a another title blog",
                "body": "this is my second blog, which is much better",
                "tags": []
            },

            "sha3": {
                "title": "a very mature title blog post ",
                "body": "We are surrounded by objects in the real world. This is my better second blog",
                "tags": []
            }
        }

        similarity_service = SimilarityService(0.7)
        similarity_map = similarity_service.find_similarity_across(input_documents)
        logger.info(similarity_map)
        expected_similarity = {
            "sha1": ["sha2"],
            "sha2": ["sha1", "sha3"],
            "sha3": ["sha2"]
        }
        self.assertEqual(set(similarity_map["sha1"]), set(expected_similarity["sha1"]))
        self.assertEqual(set(similarity_map["sha2"]), set(expected_similarity["sha2"]))
        self.assertEqual(set(similarity_map["sha3"]), set(expected_similarity["sha3"]))
