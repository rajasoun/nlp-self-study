from collections import defaultdict


class TokensSpace():
    def __init__(self, tokens=None):
        self.tokens = tokens
        if self.tokens is not None:
            self.token_to_frequency, self.token_2_id = self.compute_token_2_id_mapping(tokens)

    def compute_token_2_id_mapping(self, tokens):
        token_to_frequency = defaultdict(int)
        for token in tokens:
            token_to_frequency[token] += 1
        sorted_unique_tokens = sorted(token_to_frequency.keys())
        token_2_id_map = dict([(key, id) for id, key in enumerate(sorted_unique_tokens)])
        return token_to_frequency, token_2_id_map

    def vectorize(self, tokens):
        vector = [0] * len(self.token_2_id.keys())
        for token in tokens:
            vector[self.token_2_id[token]] = self.token_to_frequency[token]
        return vector

    def vector(self):
        return self.vectorize(self.tokens)
