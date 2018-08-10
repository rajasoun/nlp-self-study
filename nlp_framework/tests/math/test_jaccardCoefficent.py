from unittest import TestCase
from stats import JaccardCoefficient
from stats import jaccard_coefficient


class TestJaccardCoefficient(TestCase):
    def test_should_compute_when_there_is_intersection(self):
        jaccard_coefficient = JaccardCoefficient()

        tokens = ["blog", "comment", "first"]
        other_tokens = ["comment", "other", "machine", "second"]

        coefficient = jaccard_coefficient.compute(tokens, other_tokens)

        self.assertEqual(coefficient, 0.1667)

    def test_should_compute_when_there_is_no_intersection(self):
        jaccard_coefficient = JaccardCoefficient()

        tokens = ["blog", "mycomment", "first"]
        other_tokens = ["comment", "other", "machine", "second"]

        coefficient = jaccard_coefficient.compute(tokens, other_tokens)

        self.assertEqual(coefficient, 0)

    def test_should_compute_when_one_of_the_sets_is_empty(self):
        jaccard_coefficient = JaccardCoefficient()

        tokens = []
        other_tokens = ["comment", "other", "machine", "second"]

        coefficient = jaccard_coefficient.compute(tokens, other_tokens)

        self.assertEqual(coefficient, 0)

    def test_should_compute_when_both_sets_are_empty(self):
        jaccard_coefficient = JaccardCoefficient()

        tokens = []
        other_tokens = []

        coefficient = jaccard_coefficient.compute(tokens, other_tokens)

        self.assertEqual(coefficient, 0)

    def test_should_calculate_jaccard_coefficients(self):
        a_set = [1, 2, 3, 4, 5]
        other_set = [3, 4, 5, 6, 7]
        expected_co_efficient = round(3 / 7.0, 4)
        actual_co_efficient = jaccard_coefficient(a_set, other_set)
        self.assertEquals(actual_co_efficient, expected_co_efficient)

    def test_should_calculate_jaccard_coefficients_for_empty_sets(self):
        a_set = []
        other_set = []
        expected_co_efficient = 0
        actual_co_efficient = jaccard_coefficient(a_set, other_set)
        self.assertEquals(actual_co_efficient, expected_co_efficient)
