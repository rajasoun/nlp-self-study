from collections import defaultdict

from text import TextProcessor

from stats import jaccard_coefficient, CosineSimilarity
from summary.core import TokensSpace
from trinity import Logger


logger = Logger.get_logger("ResourceSimilarityService")


def similarity_co_efficient((value1, value2), text_processor=TextProcessor()):
    a_text_value = value1["value"]
    other_text_value = value2["value"]
    if (not (isinstance(a_text_value, str) or isinstance(a_text_value, unicode) or isinstance(a_text_value, list))) or (
    not (isinstance(other_text_value, str)or isinstance(other_text_value, unicode) or isinstance(other_text_value, list))):
        return 0
    if not isinstance(a_text_value, list):
        a_text_value = text_processor.tokenize(value1["value"])
    if not isinstance(other_text_value, list):
        other_text_value = text_processor.tokenize(value2["value"])

    return _co_efficient_calculation_mechanism(a_text_value)(a_text_value, other_text_value)


def _co_efficient_calculation_mechanism(field_value, TOKENS_LENGTH_THRESHOLD=10):
    return jaccard_coefficient if len(field_value) < TOKENS_LENGTH_THRESHOLD else cosine_similarity


def _vectorise(a_token_list, other_token_list):
    all_tokens = set(a_token_list).union(set(other_token_list))
    space = TokensSpace(all_tokens)
    a_vector = space.vectorize(a_token_list)
    other_vector = space.vectorize(other_token_list)
    return a_vector, other_vector


def cosine_similarity(value1, value2, similarity_calculator=CosineSimilarity()):
    return similarity_calculator.compute(*_vectorise(value1, value2))


def _common_fields(field_list, other_field_list, ignored_fields=["id"]):
    return list(set(field_list).intersection(set(other_field_list)).difference(set(ignored_fields)))


def _common_field_tuples(resource1, resource2, common_fields):
    return map(lambda field: (resource1[field], resource2[field]), common_fields)


def _field_weight(resource, field):
    return resource[field]["weight"] if "weight" in resource[field] else 1


def _field_weight_vector(resource1, resource2, common_fields):
    return map(lambda (i, field): round((_field_weight(resource1, field) + _field_weight(resource2, field)) / 2.0, 4),
               enumerate(common_fields))


def resource_similarity_weight(resource1, resource2):
    """
            Calculate Similarity weight between similarity weight
    """

    common_fields = _common_fields(resource1, resource2)
    similarity_co_efficients = map(similarity_co_efficient, _common_field_tuples(resource1, resource2, common_fields))
    corresponding_field_weights = _field_weight_vector(resource1, resource2, common_fields)
    similarity_weights = map(lambda (x, y): x * y, zip(similarity_co_efficients, corresponding_field_weights))
    similarity_weight = round(sum(similarity_weights) / float(sum(corresponding_field_weights)), 4)
    logger.info(
        "Similarity Score between resource %s and %s is %f" % (resource1["id"], resource2["id"], similarity_weight))
    return similarity_weight


def check_threshold(resource_similarity_score, similarity_threshold):
    return resource_similarity_score > similarity_threshold


def filtered_resource_combinations(all_resource_combinations, similarity_threshold):
    return filter(lambda resource_combination: check_threshold(resource_similarity_weight(*resource_combination),
                                                               similarity_threshold),
                  all_resource_combinations)


def resource_combinations(resources):
    """
            Generate resource pair combinations; nC2 combinations
    """

    return reduce(lambda x, y: x + y,
                  map(lambda (i, resource): [(resource, other_resource) for other_resource in resources[i + 1:]],
                      enumerate(resources)))


def all_resources_similarity(resources, similarity_threshold=0.6):
    """
            Calculate Similarity for all resources; Assuming commutative similarity holds
    """
    similarity_map = defaultdict(list)
    map(lambda resource_pair: (similarity_map[resource_pair[0]["id"]].append(resource_pair[1]["id"]),
                               similarity_map[resource_pair[1]["id"]].append(resource_pair[0]["id"])),
        filtered_resource_combinations(resource_combinations(resources), similarity_threshold))
    return similarity_map
