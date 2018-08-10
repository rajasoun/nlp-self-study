class Tokens:
    def __init__(self, tokens_map):
        self.tokens_map = tokens_map

    def to_map(self):
        mixture_map = []
        for token, probability in self.tokens_map.iteritems():
            token_mixture = {
                "value": token,
                "probability": probability
            }
            mixture_map.append(token_mixture)
        return mixture_map
