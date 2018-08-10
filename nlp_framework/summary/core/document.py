import re

import nltk
from summary.core import DocumentSummary, Summarizer
from summary.core import ProcessedDocument
from text import TextProcessor


class Document:
    def __init__(self, doc_id, text, summarizer=Summarizer(), text_processor=TextProcessor()):
        self.doc_id = doc_id
        self.text = text
        self.summarizer = summarizer
        self.text_processor = text_processor

    def summary(self):
        processed_document = self.processed_document()
        summary_sentences = self.summarizer.summarize_using_weighing_measures(processed_document)
        return DocumentSummary(self.doc_id, summary_sentences)

    def build_sentence_map(self):
        nltk_clean_html = nltk.clean_html(self.text)
        html_clean_text = re.sub(r'[^a-zA-Z0-9\s\n\.,;\?!]+', ' ', nltk_clean_html)
        # remove more than one occurrence of allowed special chars
        html_clean_text = re.sub(r'([\s\n\.,;\?!])(\1+)', r'\1', html_clean_text)
        sentences = self.text_processor.nltk_sentences(html_clean_text)
        return dict(enumerate(sentences))

    def build_tokenised_sentence_map(self, sentence_map):
        tokenised_sentence_map = dict(
            [(sentence_number, self.text_processor.tokenize(sentence)) for sentence_number, sentence in
             sentence_map.iteritems()])
        for id, tokenised_sentence in tokenised_sentence_map.items():
            if (tokenised_sentence == []):
                tokenised_sentence_map.pop(id)
        return tokenised_sentence_map

    def processed_document(self):
        sentence_map = self.build_sentence_map()
        tokenised_sentence_map = self.build_tokenised_sentence_map(sentence_map)
        tokens = []
        for (key, tokenised_sentence) in tokenised_sentence_map.iteritems():
            tokens.extend(tokenised_sentence)
        return ProcessedDocument(sentence_map=sentence_map, tokenised_sentence_map=tokenised_sentence_map,
                                 tokens=tokens)

    def is_summarizable(self):
        return self.summarizer.is_summarizable(self.processed_document())
