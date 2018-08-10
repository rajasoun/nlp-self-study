from unittest import TestCase
from tagger.core.singleton_lda_tagger import SingletonLDATagger


class TestSingletonLDATagger(TestCase):
    def test_should_check_only_one_instance_of_tagger_was_created(self):
        lda_tagger = SingletonLDATagger.lda_tagger()
        lda_tagger_another = SingletonLDATagger.lda_tagger()
        self.assertEquals(lda_tagger, lda_tagger_another)