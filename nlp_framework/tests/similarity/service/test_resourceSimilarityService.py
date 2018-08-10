from unittest import TestCase

from similarity.service.resource_similarity_service import _common_fields, _common_field_tuples, \
    _co_efficient_calculation_mechanism, resource_similarity_weight, all_resources_similarity, resource_combinations, \
    cosine_similarity
from stats import jaccard_coefficient


class TestResourceSimilarityService(TestCase):
    def test_should_get_common_fields(self):
        field_list = ["title", "content", "description"]
        other_field_list = ["name", "content", "description"]
        expected_common_fields = ["content", "description"]
        self.assertEquals(_common_fields(field_list, other_field_list), expected_common_fields)

    def test_should_emit_tuple_of_the_common_field_values(self):
        a_resource = {
            "title": {
                "value": "this is a simple title",
                "weight": 1
            },
            "description": {
                "value": "This is a simple description"
            },
            "tags": {
                "value": ["simple", "title", "description"],
                "weight": 2
            }
        }
        other_resource = {
            "title": {
                "value": "this is another simple title",
                "weight": 1
            },
            "content": {
                "value": "This is a another piece of content"
            },
            "tags": {
                "value": ["simple", "title", "body"],
                "weight": 2
            }
        }
        common_field_list = ["title", "tags"]
        expected_common_field_tuples = [({
                                             "value": "this is a simple title",
                                             "weight": 1}, {
                                             "value": "this is another simple title",
                                             "weight": 1}),
            ({
                 "value": ["simple", "title", "description"],
                 "weight": 2}, {
                 "value": ["simple", "title", "body"],
                 "weight": 2})]
        self.assertEquals(_common_field_tuples(a_resource, other_resource, common_field_list),
                          expected_common_field_tuples)

    def test_should_return_jaccard_co_efficient_for_list_type(self):
        field_value = ["tag1", "tag2", "tag3"]
        self.assertEquals(_co_efficient_calculation_mechanism(field_value), jaccard_coefficient)

    def test_should_return_jaccard_co_efficient_for_small_text_field_type(self):
        a_field_value = ["title", "whatever"]
        other_field_value = ["Batman", "is", "awesome", "billionaire", "industrialist", "whose", "parents", "were",
                             "killed", "mugger", "eight", "years", "old"]
        self.assertEquals(_co_efficient_calculation_mechanism(a_field_value), jaccard_coefficient)
        self.assertEquals(_co_efficient_calculation_mechanism(other_field_value), cosine_similarity)

    def test_should_calculate_resource_similarity_weight(self):
        a_resource = {
            "id": "sha123",
            "title": {
                "value": "this is a simple title",
                "weight": 1
            },
            "description": {
                "value": "This is a simple description"
            },
            "tags": {
                "value": ["simple", "title", "description"],
                "weight": 2
            }
        }
        other_resource = {
            "id": "sha124",
            "title": {
                "value": "this is a simple title",
                "weight": 1
            },
            "content": {
                "value": "not matching this one. Have to write a long piece of content"
            },
            "tags": {
                "value": ["simple", "title", "body"],
                "weight": 2
            }
        }
        actual_weight = resource_similarity_weight(a_resource, other_resource)
        self.assertEquals(actual_weight, 0.6667)

    def test_should_find_all_resource_combinations(self):
        # resource kind is not relevant for this test
        resources = [1, 2, 3, 4, 5]
        expected_resource_combinations = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5),
                                          (4, 5)]
        actual_resource_combinations = resource_combinations(resources)
        self.assertEquals(actual_resource_combinations, expected_resource_combinations)

    def test_should_find_similarity_across_resource(self):
        resources = [
            {
                "id": 123,
                "title": {
                    "value": "this is a simple title",
                    "weight": 1
                },
                "description": {
                    "value": "This is a simple description"
                },
                "tags": {
                    "value": ["simple", "title", "description"],
                    "weight": 2
                }
            }, {
                "id": 124,
                "title": {
                    "value": "post about batman",
                    "weight": 1
                },
                "description": {
                    "value": "Batman is awesome. A billionaire industrialist whose parents were killed by a mugger when he was eight years old. Traveling the world for several years to learn and experience the inner workings of the crimminal mind, and seeking the means to fight injustice, he later returns to Gotham and at night becomes the Batman, Gotham City's shadowy vigilante protector."
                },
                "tags": {
                    "value": ["batman", "bruce"],
                }
            },
            {
                "id": 125,
                "name": {
                    "value": "Batman Fan Group",
                    "weight": 1
                },
                "description": {
                    "value": "A billionaire industrialist whose parents were killed by a mugger when he was eight years old. Traveling the world for several years to learn and experience the inner workings of the crimminal mind, and seeking the means to fight injustice, he later returns to Gotham and at night becomes the Batman, Gotham City's shadowy vigilante protector",
                    "weight": 10
                },
                "tags": {
                    "value": ["batman", "fan"],
                    "weight": 3
                },
                "type": {
                    "value": "group"
                }
            }
        ]
        expected_similarity_map = {
            124: [125],
            125: [124]
        }
        similarity_map = all_resources_similarity(resources)
        self.assertEquals(similarity_map, expected_similarity_map)
