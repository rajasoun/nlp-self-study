from stats import CosineSimilarity, JaccardCoefficient


class SimilarityMeasureFactory():
    def cosine(self):
        return CosineSimilarity()

    def jaccard(self):
        return JaccardCoefficient()
