import os
import threading
from collections import defaultdict

import cPickle
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from lockfile import FileLock
from trinity import Logger

logger = Logger.get_logger("LDATagger")


class LDATagger:
    _lda_model = None
    _dictionary = None
    _lda_model_path = None
    _dictionary_path = None
    DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")
    DEFAULT_NUM_TOPICS = 1000

    def __init__(self, model_path=DEFAULT_MODEL_PATH, num_topics=DEFAULT_NUM_TOPICS, lock=threading.Lock()):
        self.save_model_lock = lock

        if os.path.isfile(model_path):
            raise Exception("Invalid Model Path; Should Be a Directory")
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        self._lda_model_path = os.path.join(model_path, "lda.model")
        self._dictionary_path = os.path.join(model_path, "tokens.dict")
        self.num_topics = num_topics
        self.model_folder_lock = FileLock(model_path)

    def topics_for_documents(self, doc_tokens_map):
        self.check_and_load_model()
        doc_topics_map = defaultdict(list)
        for document_id, document_tokens in doc_tokens_map.iteritems():
            doc_topics_map[document_id] = self.topics_for_document(document_tokens)
        return doc_topics_map

    def topics_for_document(self, tokens):
        self.check_and_load_model()
        bow_tokens = self._dictionary.doc2bow(tokens)
        topics = self._lda_model[bow_tokens]
        return topics

    def build_topics(self, tokens_list):
        self._dictionary = Dictionary(tokens_list)
        corpus = [self._dictionary.doc2bow(document_tokens) for document_tokens in tokens_list]
        self._lda_model = LdaModel(corpus=corpus, id2word=self._dictionary, num_topics=self.num_topics, passes=100)
        self.save_model()

    def save_model(self, sleep_for_test=False, mock_datastruct=None):
        self.save_model_lock.acquire()
        self.model_folder_lock.acquire()
        if mock_datastruct: mock_datastruct.acquire()
        if sleep_for_test:
            import time
            time.sleep(1)
        print
        "Acquired Lock "
        try:
            self._lda_model.save(self._lda_model_path)
            self._dictionary.save(self._dictionary_path)
        finally:
            print
            "Released Lock"
            if mock_datastruct: mock_datastruct.release()
            self.model_folder_lock.release()
            self.save_model_lock.release()

    def check_and_load_model(self):
        if self._lda_model and self._dictionary:
            return
        if os.path.exists(self._lda_model_path):
            self._lda_model = LdaModel.load(self._lda_model_path)
        else:
            raise Exception("LDA Model Not found in the path")
        if os.path.exists(self._dictionary_path):
            self._dictionary = Dictionary.load(self._dictionary_path)
        else:
            raise Exception("Tokens Dictionary Not found in the path")

    def update_model(self, tokens_list):
        self.check_and_load_model()
        corpus = [self._dictionary.doc2bow(document_tokens) for document_tokens in tokens_list]
        self._lda_model.update(corpus=corpus)
        self.save_model()

    def build_or_update_model(self, tokens_list):
        if not self.does_model_exist():
            self.build_topics(tokens_list)
        else:
            self.update_model(tokens_list)

    def does_model_exist(self):
        if os.path.exists(self._lda_model_path) and os.path.exists(self._dictionary_path):
            return True
        return False

    def get_model(self):
        self.check_and_load_model()
        model_hash = {"lda_model": cPickle.dumps(self._lda_model), "dictionary": cPickle.dumps(self._dictionary)}
        return model_hash

    def restore_model(self, model_hash):
        self._lda_model = cPickle.loads(model_hash["lda_model"].encode('utf-8'))
        self._dictionary = cPickle.loads(model_hash["dictionary"].encode('utf-8'))
        self.save_model()

    def topics_to_tokens(self):
        topics_tokens_map = defaultdict(list)
        if not self.does_model_exist():
            return []
        else:
            model = self._lda_model
            topics_to_tokens = model.show_topics(topics=self.DEFAULT_NUM_TOPICS, topn=25, log=False, formatted=False)

            for topic_id, tokens in enumerate(topics_to_tokens):
                topics_tokens_map[topic_id] = self.list_of_tuples_to_hash(tokens)

            return topics_tokens_map

    def list_of_tuples_to_hash(self, tokens):
        tokens_hash = defaultdict(float)
        for token_probability, token in tokens:
            tokens_hash[token] = token_probability
        return tokens_hash
