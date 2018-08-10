from unittest import TestCase
from mockito import spy
from summary.core import TokensSpace


class TokenSpaceTest(TestCase):
    def test_shouldComputeDocumentSpaceAsToken2IdMapping(self):
        document_tokens = ["quick", "brown", "fox", "jump", "lazy", "dog", "quick", "brown", "fox", "jump", "lazy",
                           "cat"]
        expected_token_2_id_map = {
            "brown": 0,
            "cat": 1,
            "dog": 2,
            "fox": 3,
            "jump": 4,
            "lazy": 5,
            "quick": 6,
        }
        expected_token_2_frequency_map = {
            "brown": 2,
            "cat": 1,
            "dog": 1,
            "fox": 2,
            "jump": 2,
            "lazy": 2,
            "quick": 2,
        }
        space = TokensSpace()
        actual_token_maps = space.compute_token_2_id_mapping(document_tokens)
        self.assertEquals(actual_token_maps, (expected_token_2_frequency_map, expected_token_2_id_map))


    def test_shouldCreateVectorsFromTokens(self):
        document_tokens = ["quick", "brown", "fox", "jump", "lazy", "dog", "quick", "brown", "fox", "jump", "lazy",
                           "cat"]
        document_space = TokensSpace(tokens=document_tokens)
        expected_vector = [2, 0, 0, 2, 0, 0, 2]
        sentence_tokens = ["quick", "brown", "fox"]
        actual_vector = document_space.vectorize(sentence_tokens)
        self.assertEquals(actual_vector, expected_vector)