from math import sqrt
from unittest import TestCase

from summary.core import Document
from text import TextProcessor
from util import read_text_corpus


class SentenceCohesionExperiment(TestCase):
    test_data_directory = "../test_data/sentences_cohesion"
    summarizability_map = {
        "summarizable": True,
        "non-summarizable": False
    }

    def setUp(self):
        self.text_corpus = read_text_corpus(self.test_data_directory)

    def test_should_check_whether_sentences_are_cohesive_using_standard_deviation_of_sentence_weights(self):
        text_processor = TextProcessor()
        for name, document_content in self.text_corpus.iteritems():
            document = Document(name, document_content, text_processor=text_processor)
            processed_document = document.processed_document()
            weight_map = processed_document.sentence_weight_map()
            cohesion = self.get_sentences_cohesion(weight_map)
            print
            "########################################################################"
            print
            "SentenceWeights - Cohesion for docId:%s, length: %d is %s" % (
                str(name), processed_document.number_of_sentences(), str(cohesion))
            print
            "########################################################################"

    def test_should_check_whether_sentences_are_cohesive_using_standard_deviation_of_sentence_distance_from_document(
            self):
        text_processor = TextProcessor()
        for name, document_content in self.text_corpus.iteritems():
            document = Document(name, document_content, text_processor=text_processor)
            processed_document = document.processed_document()
            weight_map = processed_document.sentence_document_distance_map()
            cohesion = self.get_sentences_cohesion_distance(weight_map)
            print
            "########################################################################"
            print
            "SentenceDistance - Cohesion for docId:%s, length: %d is %s " % (
                str(name), processed_document.number_of_sentences(), str(cohesion))
            print
            "########################################################################"

    def test_should_check_whether_sentences_are_cohesive_using_standard_deviation_of_sentence_distance_from_centroid(
            self):
        text_processor = TextProcessor()
        for name, document_content in self.text_corpus.iteritems():
            document = Document(name, document_content, text_processor=text_processor)
            processed_document = document.processed_document()
            weight_map = processed_document.sentence_centroid_distance_map()
            cohesion = self.get_sentences_cohesion_distance(weight_map)
            print
            "########################################################################"
            print
            "Centroid - Cohesion for docId:%s, length: %d is %s" % (
                str(name), processed_document.number_of_sentences(), str(cohesion))
            print
            "########################################################################"

    def test_should_check_whether_sentences_are_cohesive_using_standard_deviation_sentence_length(
            self):
        text_processor = TextProcessor()
        for name, document_content in self.text_corpus.iteritems():
            document = Document(name, document_content, text_processor=text_processor)
            processed_document = document.processed_document()
            weight_map = processed_document.sentence_length_map()
            cohesion = self.get_sentences_cohesion_distance(weight_map)
            print
            "########################################################################"
            print
            "SentenceLength - Cohesion for docId:%s, length: %d is %s " % (
                str(name), processed_document.number_of_sentences(), str(cohesion))
            print
            "########################################################################"

    def test_should_check_whether_the_document_is_summarisable(self):
        text_processor = TextProcessor()
        correct_classification = 0
        document_classified_count = {
            "summarizable": {
                "correct": 0,
                "all": 0
            },
            "non-summarizable": {
                "correct": 0,
                "all": 0
            }
        }
        for name, document_content in self.text_corpus.iteritems():
            document = Document(name, document_content, text_processor=text_processor)
            summarizability = document.is_summarizable()
            document_type = self.document_type(name)
            document_classified_count[document_type]["all"] += 1
            if self.summarizability_map[document_type] == summarizability:
                correct_classification += 1
                document_classified_count[document_type]["correct"] += 1
            print
            "########################################################################"
            print
            "Document id ", name, "Summarizability:", summarizability
        print
        "############################# Summary ##################################"
        print
        "Number of Documents: ", len(self.text_corpus)
        print
        "Number of Correctly Identified Document: ", correct_classification
        print
        "Accuracy", correct_classification / float(len(self.text_corpus))
        print
        "Precision - Summarizable: ", document_classified_count["summarizable"]["correct"] / float(
            document_classified_count["summarizable"]["all"])
        print
        "Precision - Non - Summarizable: ", document_classified_count["non-summarizable"]["correct"] / float(
            document_classified_count["non-summarizable"]["all"])
        print
        "########################################################################"

    def get_sentences_cohesion(self, weight_map):
        avg = reduce(lambda item1, item2: item1 + item2, weight_map.values()) / float(len(weight_map.values()))
        delta_from_avg = [(avg - value) for value in weight_map.values()]
        standard_deviation = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, delta_from_avg))) / len(
            delta_from_avg)
        return standard_deviation

    def get_sentences_cohesion_distance(self, weight_map):
        avg = reduce(lambda item1, item2: item1 + item2, weight_map.values()) / float(max(weight_map.values()))
        delta_from_avg = [(avg - value) for value in weight_map.values()]
        standard_deviation = sqrt(reduce(lambda x, y: x + y, map(lambda x: x * x, delta_from_avg))) / len(
            delta_from_avg)
        return standard_deviation

    def document_type(self, name):
        if name.startswith("non"):
            return "non-summarizable"
        return "summarizable"
