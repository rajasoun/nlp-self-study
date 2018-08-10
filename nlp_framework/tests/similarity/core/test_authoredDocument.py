from unittest import TestCase

from mockito import mock, when, verify, verifyNoMoreInteractions
from similarity.core import AuthoredDocument
from stats import CosineSimilarity, JaccardCoefficient


class TestAuthoredDocument(TestCase):
    def test_should_compute_title_similarity(self):
        text_processor = mock()
        similarity_measure_factory = mock()
        when(similarity_measure_factory).jaccard().thenReturn(JaccardCoefficient())
        when(text_processor).tokenize("this is a title").thenReturn(["title"])
        when(text_processor).tokenize("this is a another title blog").thenReturn(["title", "blog"])

        authored_document = AuthoredDocument("1", {"title": "this is a title", "body": "", "tags": []},
                                             text_processor=text_processor,
                                             similarity_measure_factory=similarity_measure_factory)
        other_authored_document = AuthoredDocument("2",
                                                   {"title": "this is a another title blog", "body": "", "tags": []},
                                                   text_processor=text_processor,
                                                   similarity_measure_factory=similarity_measure_factory)

        score = authored_document.title_similarity_score(other_authored_document)

        self.assertEqual(score, 0.5)
        verify(similarity_measure_factory).jaccard()
        verify(text_processor).tokenize("this is a title")
        verify(text_processor).tokenize("this is a another title blog")
        verifyNoMoreInteractions(text_processor)
        verifyNoMoreInteractions(similarity_measure_factory)

    def test_should_compute_body_similarity(self):
        text_processor = mock()
        similarity_measure_factory = mock()
        when(similarity_measure_factory).cosine().thenReturn(CosineSimilarity())
        when(text_processor).tokenize("this is my second blog, which is much better").thenReturn(["second", "blog"])
        when(text_processor).tokenize(
            "We are surrounded by objects in the real world. These can be cars, houses, etc. This is my better second blog") \
            .thenReturn(["surrounded", "objects", "real", "world", "cars", "houses", "second", "blog"])

        authored_document = AuthoredDocument("1", {"title": "this is a title",
                                                   "body": "this is my second blog, which is much better", "tags": []},
                                             text_processor=text_processor,
                                             similarity_measure_factory=similarity_measure_factory)
        other_authored_document = AuthoredDocument("2",
                                                   {"title": "this is a another title blog",
                                                    "body": "We are surrounded by objects in the real world. These can be cars, houses, etc. This is my better second blog",
                                                    "tags": []},
                                                   text_processor=text_processor,
                                                   similarity_measure_factory=similarity_measure_factory)

        score = authored_document.body_similarity_score(other_authored_document)

        verify(similarity_measure_factory).cosine()
        verify(text_processor).tokenize("this is my second blog, which is much better")
        verify(text_processor).tokenize(
            "We are surrounded by objects in the real world. These can be cars, houses, etc. This is my better second blog")
        verifyNoMoreInteractions(text_processor)
        verifyNoMoreInteractions(similarity_measure_factory)

    def test_should_compute_tags_similarity(self):
        text_processor = mock()
        similarity_measure_factory = mock()
        when(similarity_measure_factory).jaccard().thenReturn(JaccardCoefficient())

        authored_document = AuthoredDocument("1", {"title": "this is a title",
                                                   "body": "this is my second blog, which is much better",
                                                   "tags": ["second", "blog"]},
                                             text_processor=text_processor,
                                             similarity_measure_factory=similarity_measure_factory)
        other_authored_document = AuthoredDocument("2",
                                                   {"title": "this is a another title blog",
                                                    "body": "We are surrounded by objects in the real world. These can be cars, houses, etc. This is my better second blog",
                                                    "tags": ["objects", "blog", "cars", "houses"]},
                                                   text_processor=text_processor,
                                                   similarity_measure_factory=similarity_measure_factory)

        score = authored_document.tags_similarity_score(other_authored_document)

        self.assertEqual(score, 0.2000)
        verify(similarity_measure_factory).jaccard()
        verifyNoMoreInteractions(text_processor)
        verifyNoMoreInteractions(similarity_measure_factory)

    def test_should_compute_tags_similarity_when_tags_are_empty(self):
        text_processor = mock()
        similarity_measure_factory = mock()
        when(similarity_measure_factory).jaccard().thenReturn(JaccardCoefficient())

        authored_document = AuthoredDocument("1", {"title": "this is a title",
                                                   "body": "this is my second blog, which is much better",
                                                   "tags": []},
                                             text_processor=text_processor,
                                             similarity_measure_factory=similarity_measure_factory)
        other_authored_document = AuthoredDocument("2",
                                                   {"title": "this is a another title blog",
                                                    "body": "We are surrounded by objects in the real world. These can be cars, houses, etc. This is my better second blog",
                                                    "tags": []},
                                                   text_processor=text_processor,
                                                   similarity_measure_factory=similarity_measure_factory)

        score = authored_document.tags_similarity_score(other_authored_document)

        self.assertEqual(score, 0)
        verify(similarity_measure_factory).jaccard()
        verifyNoMoreInteractions(text_processor)
        verifyNoMoreInteractions(similarity_measure_factory)

    def test_should_compute_weighted_sum_of_coefficients(self):
        text_processor = mock()
        similarity_measure_factory = mock()

        authored_document = AuthoredDocument("1", {"title": "",
                                                   "body": "",
                                                   "tags": []},
                                             text_processor=text_processor,
                                             similarity_measure_factory=similarity_measure_factory)
        weighted_sum = authored_document.weighted_sum(title_score=0.5, body_score=0.6, tag_score=0.6)
        self.assertEqual(weighted_sum, 0.6)
