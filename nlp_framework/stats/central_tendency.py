import sys
from numpy import sqrt


def square(x):
    return x ** 2


def standard_deviation(avg, observations):
    delta_from_avg = [(avg - value) for value in observations]
    if len(delta_from_avg) == 0:
        return float(sys.maxint)
    return sqrt(sum(map(square, delta_from_avg))) / float(len(
        delta_from_avg))


def weight_deviation(weight_map):
    if not bool(weight_map):
            return float(sys.maxint)
    avg = sum(weight_map.values()) / float(len(weight_map.values()))
    return round(standard_deviation(avg, weight_map.values())/float(avg), 4)


def distance_deviation(distance_map):
    if not bool(distance_map):
            return float(sys.maxint)
    max_distance = max(distance_map.values())
    if max_distance <= 0:
        return float(sys.maxint)
    avg = sum(distance_map.values()) / float(max_distance)
    return round(standard_deviation(avg, distance_map.values())/float(avg), 4)