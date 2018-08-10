from math import sqrt


def euclidean_distance(vector1, vector2):
    return round(sqrt(reduce(lambda x, y: x + y, map(lambda x: (x[1] - x[0]) ** 2, zip(vector1, vector2)))), 4)