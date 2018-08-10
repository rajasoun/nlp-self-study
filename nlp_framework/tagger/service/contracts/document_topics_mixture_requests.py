import json
from tagger.service.contracts import Topics


class DocumentTopicsMixturesRequest:
    def __init__(self, docs_topics_map, topics_tokens_map):
        self.document_topics_map = docs_topics_map
        self.topics_tokens_map = topics_tokens_map

    def to_json(self):
        mixture_json = []
        for doc_id, topics in self.document_topics_map.iteritems():
            topics = Topics(topics, self.topics_tokens_map)
            doc_topics_mixture = {
                "id": doc_id,
                "topics": topics.to_map()
            }
            mixture_json.append(doc_topics_mixture)
        return json.dumps(mixture_json)


class DocumentTopicsMixtureRequest:
    def __init__(self, document_id, topics, topics_tokens_map):
        self.document_id = document_id
        self.topics = topics
        self.topics_tokens_map = topics_tokens_map

    def to_json(self):
        topics = Topics(self.topics, self.topics_tokens_map)
        doc_topics_mixture = {
                "id": self.document_id,
                "topics": topics.to_map()
            }
        return json.dumps(doc_topics_mixture)