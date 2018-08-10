from collections import defaultdict

from stats import CosineSimilarity, euclidean_distance
from summary.core import TokensSpace
from text import TextProcessor


class ProcessedDocument:
    ALPHA = 5
    BETA = 1

    def __init__(self, sentence_map, tokenised_sentence_map, tokens):
        self.sentence_map = sentence_map
        self.tokenised_sentence_map = tokenised_sentence_map
        self.tokens = tokens
        self.document_space = TokensSpace(tokens=tokens)

    def pop_tokenised_sentence(self, index):
        return self.tokenised_sentence_map.pop(index)

    def sentence(self, index):
        return self.sentence_map[index]

    def sentence_cosine_similarity_weight(self, sentence_tokens):
        sentence_vector = self.document_space.vectorize(sentence_tokens)
        return CosineSimilarity().compute(sentence_vector, self.document_space.vectorize(self.tokens))

    def sentence_cosine_similarity_map(self):
        sentence_similarity_map = defaultdict(float)
        for sentence_number, sentence_tokens in self.tokenised_sentence_map.iteritems():
            sentence_similarity_map[sentence_number] = self.sentence_cosine_similarity_weight(sentence_tokens)
        return sentence_similarity_map

    def sentence_weight_map(self):
        sentence_weight_map = defaultdict(float)
        for sentence_number, sentence_tokens in self.tokenised_sentence_map.iteritems():
            cosine_weight = self.cosine_similarity_weight_for(sentence_number)
            noun_weights = self.weight_by_nouns(sentence_number)
            weighted_sum = self.ALPHA * cosine_weight + self.BETA * noun_weights
            sentence_weight_map[sentence_number] = weighted_sum
        return sentence_weight_map

    def eliminate_processed_sentence(self, sentence_id):
        sentence_tokens = self.pop_tokenised_sentence(sentence_id)
        self.tokens = filter(lambda token: token not in sentence_tokens, self.tokens)

    def number_of_sentences(self):
        return len(self.sentence_map.keys())

    def nouns_in(self, sentence_id, text_processor=TextProcessor()):
        return text_processor.nouns(self.tokenised_sentence_map[sentence_id])

    def sentence_length(self, sentence_id):
        return len(self.tokenised_sentence_map[sentence_id])

    def cosine_similarity_weight_for(self, sentence_id):
        sentence_tokens = self.tokenised_sentence_map[sentence_id]
        return self.sentence_cosine_similarity_weight(sentence_tokens)

    def weight_by_nouns(self, sentence_id):
        nouns = self.nouns_in(sentence_id)
        return round(len(nouns) / float(self.sentence_length(sentence_id)), 4)

    def sentence_document_distance(self, sentence_id):
        sentence_vector = self.document_space.vectorize(self.tokenised_sentence_map[sentence_id])
        document_vector = self.document_space.vector()
        return euclidean_distance(sentence_vector, document_vector)

    def sentence_document_distance_map(self):
        sentence_document_map = defaultdict(float)
        for sentence_number in self.tokenised_sentence_map.keys():
            sentence_document_map[sentence_number] = self.sentence_document_distance(sentence_number)
        return sentence_document_map

    def sentence_centroid_distance_map(self):
        all_vectors = dict([(sentence_number, self.sentence_vector(sentence_number)) for sentence_number in
                            self.tokenised_sentence_map.keys()])
        centroid = self.centroid_of_document(all_vectors.values())
        sentence_centroid_map = defaultdict(float)
        for sentence_number, vector in all_vectors.iteritems():
            sentence_centroid_map[sentence_number] = euclidean_distance(vector, centroid)
        return sentence_centroid_map

    def sentence_length_map(self):
        return dict(
            [(sentence_number, len(tokens)) for sentence_number, tokens in self.tokenised_sentence_map.iteritems()])

    def __eq__(self, other):
        if isinstance(other, ProcessedDocument):
            is_equal = self.sentence_map == other.sentence_map and \
                       self.tokenised_sentence_map == other.tokenised_sentence_map and \
                       len(self.tokens) == len(other.tokens) and \
                       set(self.tokens) == set(other.tokens)
            return is_equal
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def sentence_vector(self, sentence_number):
        return self.document_space.vectorize(self.tokenised_sentence_map[sentence_number])

    def centroid_of_document(self, all_vectors):
        if not all_vectors:
            return []
        return map(lambda sum_i_vector: sum_i_vector / float(len(all_vectors)), reduce(
            lambda vector1, vector2: map(lambda (xi, yi): xi + yi, zip(vector1, vector2)),
            all_vectors))
