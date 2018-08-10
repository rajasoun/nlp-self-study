from math import sqrt

'''Ref: http://en.wikipedia.org/wiki/Cosine_similarity'''


class CosineSimilarity:
    def compute(self, vectorA, vectorB):
        if len(vectorA) == 0 or len(vectorB) == 0: return 0
        dot_product = reduce(lambda x, y: x + y, map(lambda Ai, Aj: Ai * Aj, vectorA, vectorB))
        vectorA_norm = sqrt(reduce(lambda x, y: x + y, map(lambda Ai: Ai * Ai, vectorA)))
        vectorB_norm = sqrt(reduce(lambda x, y: x + y, map(lambda Bi: Bi * Bi, vectorB)))
        denominator = float(vectorA_norm * vectorB_norm)
        if denominator == 0: return 0
        cosine_similarity_score = dot_product / denominator
        return round(cosine_similarity_score, 4)
