from stats import SimilarityMeasureFactory
from summary.core import TokensSpace
from text import TextProcessor


class AuthoredDocument():
    def __init__(self, doc_id, document_map, text_processor=TextProcessor(),
                 similarity_measure_factory=SimilarityMeasureFactory()):
        self.doc_id = doc_id
        self.title = document_map["title"]
        self.body = document_map["body"]
        self.tags = document_map["tags"] if document_map.has_key("tags") else []
        self.text_processor = text_processor
        self.similarity_measure_factory = similarity_measure_factory

    def similarity_score(self, other_authored_document):
        title_score = self.title_similarity_score(other_authored_document)
        body_score = self.body_similarity_score(other_authored_document)
        tags_score = self.tags_similarity_score(other_authored_document)
        return self.weighted_sum(title_score, body_score, tags_score)

    def title_similarity_score(self, other_authored_document):
        tokens = self.text_processor.tokenize(self.title)
        other_tokens = self.text_processor.tokenize(other_authored_document.title)

        return self.similarity_measure_factory.jaccard().compute(tokens, other_tokens)

    def body_similarity_score(self, other_authored_document):
        tokens = self.text_processor.tokenize(self.body)
        other_tokens = self.text_processor.tokenize(other_authored_document.body)
        all_document_tokens = tokens + other_tokens
        space = TokensSpace(tokens=all_document_tokens)

        vector = space.vectorize(tokens)
        other_vector = space.vectorize(other_tokens)
        return self.similarity_measure_factory.cosine().compute(vector, other_vector)

    def tags_similarity_score(self, other_authored_document):
        tokens = self.tags
        other_tokens = other_authored_document.tags
        return self.similarity_measure_factory.jaccard().compute(tokens, other_tokens)

    def weighted_sum(self, title_score, body_score, tag_score):
        TITLE_THRESHOLD = 0.8
        TAG_THRESHOLD = 0.5
        normalizer = 4
        weighted_score = 4 * body_score
        if title_score >= TITLE_THRESHOLD:
            weighted_score += 2 * title_score
            normalizer += 2
        if tag_score >= TAG_THRESHOLD:
            weighted_score += 3 * tag_score
            normalizer += 3

        normalised_weighted_score = weighted_score / float(normalizer)
        return round(normalised_weighted_score, 4)



