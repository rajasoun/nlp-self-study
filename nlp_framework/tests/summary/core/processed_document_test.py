from math import sqrt
from unittest import TestCase
from mockito import mock, when
from mockito.inorder import verify
from summary.core.processed_document import ProcessedDocument


class ProcessedDocumentTest(TestCase):
    def test_shouldGetCosineSentenceSimilarity(self):
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber sentence.",
            2: "This is a dumbest sentence."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "sentence"],
            2: ["dumbest", "sentence"]
        }
        tokens = ["dumb", "sentence", "sentence", "dumber", "dumbest", "sentence"]
        processed_document = ProcessedDocument(sentence_map, tokenised_sentence_map, tokens)
        actual_sentence_cosine_similarity = processed_document.sentence_cosine_similarity_weight(["dumb", "sentence"])
        self.assertIsNotNone(actual_sentence_cosine_similarity)
        self.assertIsNot(actual_sentence_cosine_similarity, 0)

    def test_shouldGetCosineSimilarityMap(self):
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber sentence.",
            2: "This is a dumbest sentence."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "sentence"],
            2: ["dumbest", "sentence"]
        }
        tokens = ["dumb", "sentence", "sentence", "dumber", "dumbest", "sentence"]
        processed_document = ProcessedDocument(sentence_map, tokenised_sentence_map, tokens)
        actual_cosine_similarity_map = processed_document.sentence_cosine_similarity_map()
        self.assertIsNotNone(actual_cosine_similarity_map)
        for tokenised_sentence_id, similarity_value in actual_cosine_similarity_map.iteritems():
            self.assertIsNotNone(similarity_value)

    def test_should_get_nouns_for_sentence_given_id(self):
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber sentence.",
            2: "This is a Noun Sentence, noun being good Network."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "sentence"],
            2: ["noun", "sentence", "noun", "good", "network"]
        }
        noun_tokens = ["noun", "sentence", "noun", "network"]
        tokens = ["dumb", "sentence", "sentence", "dumber", "noun", "sentence", "noun", "network"]
        sentence_id = 2
        text_processor = mock()
        when(text_processor).nouns(tokenised_sentence_map[sentence_id]).thenReturn(noun_tokens)

        processed_document = ProcessedDocument(sentence_map, tokenised_sentence_map, tokens)
        processed_document.nouns_in(sentence_id, text_processor=text_processor)
        verify(text_processor).nouns(tokenised_sentence_map[sentence_id])


    def test_should_calculate_weight_given_sentence_id(self):
        sentence_map = {
            0: "This is a dumb sentence dumbest.",
            1: "This is a fast dumb sentence."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence", "dumbest"],
            1: ["fast", "dumb", "sentence"],
        }
        tokens = ["dumb", "sentence", "sentence", "fast", "dumb", "dumbest"]
        processed_document = ProcessedDocument(sentence_map=sentence_map,
                                               tokenised_sentence_map=tokenised_sentence_map,
                                               tokens=tokens)

        sentence_1_weight = processed_document.weight_by_nouns(1)
        self.assertEqual(sentence_1_weight, round(1 / float(3), 4))

    def test_should_calculate_sentence_distance_from_document(self):
        sentence_map = {
            0: "This is a dumb sentence dumbest.",
            1: "This is a fast dumb sentence.",
            2: "This is a sentence."
        }

        tokenised_sentence_map = {
            0: ["dumb", "sentence", "dumbest"],
            1: ["fast", "dumb", "sentence"],
            2: ["sentence"],
        }

        tokens = ["dumb", "sentence", "sentence", "fast", "dumb", "dumbest", "sentence"]

        processed_document = ProcessedDocument(sentence_map=sentence_map,
                                               tokenised_sentence_map=tokenised_sentence_map,
                                               tokens=tokens)

        self.assertEqual(processed_document.sentence_document_distance(0), 1)
        self.assertEqual(processed_document.sentence_document_distance(1), 1)
        self.assertEqual(processed_document.sentence_document_distance(2), round(sqrt(6), 4))






