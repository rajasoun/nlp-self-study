import os
from unittest import TestCase

import os.path as os_path
from summary.core import Summarizer, Document, ProcessedDocument


class SummarizerTest(TestCase):
    def setUp(self):
        test_content_path = os_path.join(os_path.dirname(__file__), "../test_data/test_content.txt")
        with open(test_content_path) as test_content_file:
            text = test_content_file.read()
        document = Document(doc_id=100, text=text)
        self.processed_document = document.processed_document()

    def test_shouldSummarizeContent(self):
        expected_number_of_sentences_in_summary = 3
        summarizer = Summarizer(compression_ratio=10)
        summary_sentences = summarizer.summarize_using_weighing_measures(self.processed_document)
        self.assertEquals(len(summary_sentences), expected_number_of_sentences_in_summary)

    def test_shouldGetHighestWeighedSentenceId(self):
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber dumb sentence.",
            2: "This is a dumbest sentence."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "dumb", "sentence"],
            2: ["dumbest", "sentence"]
        }
        tokens = ["dumb", "sentence", "sentence", "dumber", "dumb", "dumbest", "sentence"]
        processed_document = ProcessedDocument(sentence_map=sentence_map, tokenised_sentence_map=tokenised_sentence_map,
                                               tokens=tokens)
        expected_sentence_id = 1
        summarizer = Summarizer()
        actual_sentence_id = summarizer.highest_weighed_sentence_id(processed_document)

        self.assertEquals(actual_sentence_id, expected_sentence_id)

    def test_should_getMaxSummaryItemsBasedOnNumberOfSentencesAvailable(self):
        sentence_map = {
            0: "This is a dumb sentence dumbest.",
            1: "This is a dumber dumb sentence."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence", "dumbest"],
            1: ["dumber", "dumb", "sentence"],
        }
        tokens = ["dumb", "sentence", "sentence", "dumber", "dumb", "dumbest"]
        processed_document = ProcessedDocument(sentence_map=sentence_map,
                                               tokenised_sentence_map=tokenised_sentence_map,
                                               tokens=tokens)

        summarizer = Summarizer()
        summary = summarizer.summarize_using_weighing_measures(processed_document)
        self.assertEquals(len(summary), 2)

    def test_should_getMaxSummaryItemsBasedOnCompressionRatio(self):
        sentence_map = {
            0: "This is a dumb sentence dumbest.",
            1: "This is a dumber dumb sentence.",
            2: "This is for apple sentence.",
            3: "This is for ball sentence.",
            4: "This is for cat sentence.",
            5: "This is for dog sentence.",
            6: "This is for egg sentence.",
            7: "This is for fish sentence.",
            8: "This is for goat sentence.",
            9: "This is for hen sentence."
        }
        tokenised_sentence_map = {
            0: ["dumb", "sentence", "dumbest"],
            1: ["dumber", "dumb", "sentence"],
            2: ["apple", "sentence"],
            3: ["ball", "sentence"],
            4: ["cat", "sentence"],
            5: ["dog", "sentence"],
            6: ["egg", "sentence"],
            7: ["fish", "sentence"],
            8: ["goat", "sentence"],
            9: ["hen", "sentence"],
        }
        tokens = ["dumb", "sentence", "sentence", "dumber", "dumb", "dumbest", "apple",
                  "ball",
                  "cat",
                  "dog",
                  "egg",
                  "fish",
                  "goat",
                  "hen", ]
        processed_document = ProcessedDocument(sentence_map=sentence_map,
                                               tokenised_sentence_map=tokenised_sentence_map,
                                               tokens=tokens)
        COMPRESSION_RATIO = 10

        summarizer = Summarizer(compression_ratio=COMPRESSION_RATIO)
        summary = summarizer.summarize_using_weighing_measures(processed_document)
        self.assertEquals(len(summary), COMPRESSION_RATIO * len(sentence_map.keys()) / 100)

    def test_should_return_true_if_document_is_summerizable(self):
        text_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_data/summarisable_document.txt"))
        with open(text_file_path, "rb") as text_file:
            document_content = text_file.read()

        document = Document(text_file_path, document_content)
        processed_document = document.processed_document()
        summarizer = Summarizer()
        self.assertTrue(summarizer.is_summarizable(processed_document))

    def test_should_return_false_if_document_is_not_summerizable(self):
        text_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_data/non_summarisable_document.txt"))
        with open(text_file_path, "rb") as text_file:
            document_content = text_file.read()

        document = Document(text_file_path, document_content)
        processed_document = document.processed_document()
        summarizer = Summarizer()
        self.assertFalse(summarizer.is_summarizable(processed_document))

    def test_should_return_false_when_numericAndSymbolsFormEntireText(self):
        text_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test_data/number_random_text.txt"))
        with open(text_file_path, "rb") as text_file:
            document_content = text_file.read()

        document = Document(text_file_path, document_content)
        processed_document = document.processed_document()
        summarizer = Summarizer()
        self.assertFalse(summarizer.is_summarizable(processed_document))


