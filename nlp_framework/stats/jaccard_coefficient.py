class JaccardCoefficient():
    def compute(self, tokens, other_tokens):
        setA = set(tokens)
        setB = set(other_tokens)

        intersection = setA.intersection(setB)
        union = setA.union(setB)

        if len(union) == 0:
            return 0
        return round((len(intersection) / float(len(union))), 4)


def jaccard_coefficient(a_set, other_set):
    a_set = set(a_set)
    other_set = set(other_set)
    return round(
        (len(a_set.intersection(other_set)) /
         float(len(a_set.union(other_set)))), 4) if len(a_set.union(other_set)) > 0 else 0
