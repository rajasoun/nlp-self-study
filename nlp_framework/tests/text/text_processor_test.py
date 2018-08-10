from unittest import TestCase

from text import TextProcessor


class TestTextProcessor(TestCase):
    def test_shouldTokeniseASentence(self):
        sentence = "The quick Brown fox jumps over the lazy dog"
        expected_tokens = ["quick", "Brown", "fox", "jump", "lazy", "dog"]
        actual_tokens = TextProcessor().tokenize(sentence)
        self.assertEquals(actual_tokens, expected_tokens)

    def test_shouldTokeniseSentences(self):
        text = "Neuberger's reference is to the UN's 1948 Universal Declaration of Human Rights, which states that: \"No one shall be subjected to torture or to cruel, inhuman or degrading treatment or punishment.\" There is also the UN convention against torture, ratified by the UK in 1988."
        expected_sentences = [
            "Neuberger's reference is to the UN's 1948 Universal Declaration of Human Rights, which states that: \"No one shall be subjected to torture or to cruel, inhuman or degrading treatment or punishment",
            "\" There is also the UN convention against torture, ratified by the UK in 1988"
        ]
        actual_sentences = TextProcessor().sentences(text)
        self.assertEquals(actual_sentences, expected_sentences)

    def test_shouldGetNumberOfNamedEntities(self):
        processor = TextProcessor()
        text_sample1 = "Neuberger's reference is to the UN's 1948 Universal Declaration of Human Rights, which states that: \"No one shall be subjected to torture or to cruel, inhuman or degrading treatment or punishment"
        named_entities = ["Neuberger", "UN", "Universal", "Human Rights"]
        expected_count = len(named_entities)
        actual_count = processor.get_named_entity_count(text_sample1)
        self.assertEquals(actual_count, expected_count)

        # To show that NE is not an exact science, fails to identify 'UK'
        text_sample2 = " There is also the UN convention against torture, ratified by the UK in 1988"
        expected_count = 1
        actual_count = processor.get_named_entity_count(text_sample2)
        self.assertEquals(actual_count, expected_count)
