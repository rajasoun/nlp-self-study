from math import log

from stats import distance_deviation
from trinity import Logger

logger = Logger.get_logger("Summarizer")


class Summarizer:
    ALPHA = 1
    BETA = 1
    GAMMA = 2
    DEFAULT_COMPRESSION = 10
    NUMBER_OF_WEIGHTING_MEASURES = 3.0

    def __init__(self, compression_ratio=DEFAULT_COMPRESSION):
        self.compression_ratio = compression_ratio

    def summary_length(self, processed_document):
        compressed_length_based_on_document = processed_document.number_of_sentences() * self.compression_ratio / 100
        if (compressed_length_based_on_document == 0): return processed_document.number_of_sentences()
        return compressed_length_based_on_document

    def summarize_using_weighing_measures(self, processed_document):
        number_of_sentences_in_summary = self.summary_length(processed_document)
        summary_sentence_ids = []
        for i in range(0, number_of_sentences_in_summary):
            highest_weighed_sentence_number = self.highest_weighed_sentence_id(processed_document)
            summary_sentence_ids.append(highest_weighed_sentence_number)
            processed_document.eliminate_processed_sentence(highest_weighed_sentence_number)
        summary = [processed_document.sentence(sentence_number) for sentence_number in sorted(summary_sentence_ids)]
        return summary

    def highest_weighed_sentence_id(self, processed_document):
        FIRST = 0
        sentence_weight_map = processed_document.sentence_weight_map()
        highest_weighed_sentence_number = \
            sorted(sentence_weight_map, key=sentence_weight_map.get, reverse=True)[FIRST]
        return highest_weighed_sentence_number

    def is_summarizable(self, processed_document):
        sentence_length_map = processed_document.sentence_length_map()
        centroid_distance_map = processed_document.sentence_centroid_distance_map()
        document_distance_map = processed_document.sentence_document_distance_map()
        in_cohesion = (distance_deviation(sentence_length_map) + distance_deviation(
            centroid_distance_map) + distance_deviation(document_distance_map) + log(
            processed_document.number_of_sentences(), 300)) / float(4)
        logger.info("Incohesion  %s" % in_cohesion)
        return 0 < in_cohesion < 0.4
