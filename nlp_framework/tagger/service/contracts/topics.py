from tagger.service.contracts import Tokens

class Topics:
    def __init__(self, list_of_topics_tuple, topics_tokens_map):
        self.topics_tuples = list_of_topics_tuple
        self.topics_tokens_map = topics_tokens_map

    def to_map(self):
        mixture_map = []
        for topic_id, probability in self.topics_tuples:
            topic_mixture = {
                "id" : str(topic_id),
                "probability" : probability,
                "tokens" : Tokens(self.topics_tokens_map[topic_id]).to_map(),
                "category" : ""
            }
            mixture_map.append(topic_mixture)
        return mixture_map