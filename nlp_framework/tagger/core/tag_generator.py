import operator
from collections import defaultdict


class TagGenerator:
    def __init__(self, topics_tokens_map):
        self.topics_tokens_map = topics_tokens_map

    def generate_documents_tag_map(self, documents_tokens_map, documents_topics_map, top_n=10):
        docs_tags_map = defaultdict(list)
        for doc_id, tokens in documents_tokens_map.iteritems():
            topics = documents_topics_map[doc_id]
            docs_tags_map[doc_id] = self.generate_tags(topics=topics, tokens=tokens, top_n=top_n)
        return docs_tags_map

    def generate_tags(self, topics, tokens, top_n=10):
        weighted_tokens_map = defaultdict(float)
        for topic, probability in topics:
            topic_tokens_map = self.topics_tokens_map[topic]
            for token, weight in topic_tokens_map.iteritems():
                weighted_tokens_map[token] += weight * probability
        token_set = list(set(tokens).intersection(set(weighted_tokens_map.keys())))
        intersected_weighted_map = defaultdict(float)
        for token in token_set:
            intersected_weighted_map[token] = weighted_tokens_map[token]
        sorted_token_map = dict(
            sorted(intersected_weighted_map.iteritems(), key=operator.itemgetter(1), reverse=True)[:top_n])
        tags = sorted_token_map.keys()
        return tags
