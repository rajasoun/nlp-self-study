from unittest import TestCase
from mockito import *
from summary.core import DocumentSummary, ProcessedDocument, Summarizer
from summary.core import Document


class DocumentTest(TestCase):
    def test_shouldExtractSummary(self):
        summarizer = mock()
        document_text = "This is one summary sentence. This is what you are trying to summarize. "\
            + "In this test it does not matter what is the kind of text you supply, this is another summary sentence. "\
            + "That is because it uses a mock and is trying to test the behavior of api. The API sanity check for "\
            + "summary mechanism itself is showcased in summary test"
        document = Document(doc_id="123", text=document_text, summarizer=summarizer)
        sentence_map = {
            0: 'This is one summary sentence.',
            1: 'This is what you are trying to summarize.',
            2: 'In this test it does not matter what is the kind of text you supply, this is another summary sentence.',
            3: 'That is because it uses a mock and is trying to test the behavior of api.',
            4: 'The API sanity check for summary mechanism itself is showcased in summary test'
        }
        tokenised_sentence_map = {
            0: ['summary', 'sentence'],
            1: ['summarize'],
            2: ['test', 'matter', 'kind', 'text', 'supply', 'summary', 'sentence'],
            3: ['mock', 'test', 'behavior', 'api'],
            4: ['API', 'sanity', 'check', 'summary', 'mechanism', 'showcased', 'summary', 'test']
        }
        tokens = [
            'summary', 'sentence', 'summarize', 'test', 'matter', 'kind', 'text', 'supply', 'summary', 'sentence','mock',
            'test', 'behavior', 'api', 'API', 'sanity', 'check', 'summary', 'mechanism', 'showcased','summary', 'test'
        ]
        processed_document = ProcessedDocument(sentence_map=sentence_map, tokenised_sentence_map=tokenised_sentence_map, tokens=tokens)
        summary_sentences = ["This is one summary sentence", "this is another summary sentence"]
        expected_summary = DocumentSummary("123", summary_sentences)
        when(summarizer).summarize_using_weighing_measures(processed_document).thenReturn(summary_sentences)

        document_summary = document.summary()

        verify(summarizer).summarize_using_weighing_measures(processed_document)
        self.assertEquals(expected_summary, document_summary)

    def test_shouldBuildSentenceMap(self):
        test_text = "This is one summary sentences. This is what you are trying to summarize." \
                    + "In this test it does not matter what is the kind of text you supply, this is another summary sentence." \
                    + "That is because it uses a mock and is trying to test the behavior of api.The API sanity check for" \
                    + "summary mechanism itself is showcased in summary test"
        text_processor = mock()
        when(text_processor).nltk_sentences(test_text).thenReturn([
            "This is one summary sentences. This is what you are trying to summarize.",
            "In this test it does not matter what is the kind of text you supply, this is another summary sentence.",
            "That is because it uses a mock and is trying to test the behavior of api.The API sanity check for summary mechanism itself is showcased in summary test"
        ])
        document = Document(doc_id="123", text=test_text, text_processor=text_processor)
        expected_sentence_map = {0: "This is one summary sentences. This is what you are trying to summarize.",
                                 1: "In this test it does not matter what is the kind of text you supply, this is another summary sentence.",
                                 2: "That is because it uses a mock and is trying to test the behavior of api.The API sanity check for summary mechanism itself is showcased in summary test"}
        actual_sentence_map = document.build_sentence_map()
        self.assertEquals(actual_sentence_map, expected_sentence_map)

    def test_shouldReturnTokenisedSentencesFromSentences(self):
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber sentence.",
            2: "This is a dumbest sentence.",
            3: "This is a"
        }
        text_processor = mock()
        when(text_processor).tokenize("This is a dumb sentence.").thenReturn(["dumb", "sentence"])
        when(text_processor).tokenize("This is a dumber sentence.").thenReturn(["dumber", "sentence"])
        when(text_processor).tokenize("This is a dumbest sentence.").thenReturn(["dumbest", "sentence"])
        when(text_processor).tokenize("This is a").thenReturn([])
        expected_tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "sentence"],
            2: ["dumbest", "sentence"]
        }

        document = Document(doc_id="123", text="", text_processor=text_processor)
        actual_tokenised_sentence_map = document.build_tokenised_sentence_map(sentence_map)
        self.assertEquals(actual_tokenised_sentence_map, expected_tokenised_sentence_map)

    def test_shouldCreateProcessedDocument(self):
        test_text = "This is a dumb sentence. This is a dumber sentence. This is a dumbest sentence."
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber sentence.",
            2: "This is a dumbest sentence."
        }

        tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "sentence"],
            2: ["dumbest", "sentence"]
        }
        document_tokens = ["dumb", "sentence", "sentence", "dumber", "dumbest", "sentence" ]
        expected_processed_document = ProcessedDocument(sentence_map=sentence_map,
                                                        tokenised_sentence_map=tokenised_sentence_map,
                                                        tokens=document_tokens)
        document = Document(doc_id="123", text=test_text)
        actual_processed_document = document.processed_document()

        self.assertEquals(actual_processed_document, expected_processed_document)

    def test_should_check_if_document_is_summarisable(self):
        mock_summarizer = mock(Summarizer())
        test_text = "This is a dumb sentence. This is a dumber sentence. This is a dumbest sentence."
        sentence_map = {
            0: "This is a dumb sentence.",
            1: "This is a dumber sentence.",
            2: "This is a dumbest sentence."
        }

        tokenised_sentence_map = {
            0: ["dumb", "sentence"],
            1: ["dumber", "sentence"],
            2: ["dumbest", "sentence"]
        }
        document_tokens = ["dumb", "sentence", "sentence", "dumber", "dumbest", "sentence" ]
        processed_document = ProcessedDocument(sentence_map=sentence_map,
                                                        tokenised_sentence_map=tokenised_sentence_map,
                                                        tokens=document_tokens)
        document = Document(doc_id="123", text=test_text, summarizer=mock_summarizer)
        when(mock_summarizer).is_summarizable(processed_document).thenReturn(True)
        document.is_summarizable()
        verify(mock_summarizer).is_summarizable(processed_document)
