import json

from tagger.service.contracts import Tokens


class TopicTokensMixturesRequest():
    def __init__(self, topics_tokens_map):
        self.topics_tokens_map = topics_tokens_map

    def to_json(self):
        mixture_json = []
        for topic_id, tokens_map in self.topics_tokens_map.iteritems():
            tokens = Tokens(tokens_map)
            topic_tokens_mixture = {
                "topicId": topic_id,
                "tokens": tokens.to_map()
            }
            mixture_json.append(topic_tokens_mixture)
        return json.dumps(mixture_json)
