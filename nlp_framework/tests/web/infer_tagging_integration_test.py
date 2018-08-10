import json
import os
import os.path as os_path
import shutil
import unittest

from tagger.config import load, config
from tagger.core import LDATagger
from tagger.service.contracts import DocumentsResponse
from tests.web import StubHTTPServer
from tornado.testing import AsyncHTTPTestCase
from trinity import Logger
from web import TrinityApp

logger = Logger.get_logger("InferTaggingIntegrationTest")


class InferTaggingIntegrationTest(AsyncHTTPTestCase):
    """
            Assumes that there is and exiting model which has representation of generated topics.
            Expressed by creating a model in the setUp phase
    """

    config_path = os_path.join(os_path.abspath(os_path.dirname(__file__)), "config.yml")
    stub_http_server = None
    document_response = {
        "id": "10",
        "tokens": ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication"]
    }

    document_id = json.dumps({
        "documentId": "10"
    })

    @classmethod
    def setUpClass(cls):
        cls.stub_http_server = StubHTTPServer(1111)
        cls.stub_http_server.start()
        load(cls.config_path)

    @classmethod
    def tearDownClass(cls):
        cls.stub_http_server.stop()

    def setUp(self):
        super(InferTaggingIntegrationTest, self).setUp()
        self.clear_model(config("app.model_path"))

        self.generate_a_model_for_inference()
        self.stub_http_server.reset()

    def tearDown(self):
        super(InferTaggingIntegrationTest, self).tearDown()
        self.clear_model(config("app.model_path"))

    def get_app(self):
        return TrinityApp(self.config_path)

    def test_should_infer_topics_for_document(self):
        content_store_stub_server = self.stub_http_server

        document_request = "/document/%s/tokens" % json.loads(self.document_id)["documentId"]
        content_store_stub_server.response_when(method="GET",
                                                path=document_request,
                                                response=json.dumps(self.document_response),
                                                responseType="application/json")

        response = self.fetch("/tagger/document", method="POST", body=self.document_id)

        self.assertTrue(
            content_store_stub_server.request_received(method="GET", path=document_request))
        self.assertTrue(content_store_stub_server.request_received(method="POST", path="/document/logical_topics"))
        self.assertTrue(content_store_stub_server.request_received(method="POST", path="/document/tags"))

        self.assertEqual(200, response.code)
        self.assertEqual('success', json.loads(response.body)["status"])

    def clear_model(self, test_model_path):
        if os.path.exists(test_model_path):
            shutil.rmtree(test_model_path)

    def generate_a_model_for_inference(self):
        documents_response_map = [
            {
                "id": "1",
                "tokens": ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication",
                           "content",
                           "network", "router", "wifi", "cable", "ethernet", "socket", "authentication"]
            },
            {
                "id": "2",
                "tokens": ["java", "golang", "cool", "awesome"]
            },
            {
                "id": "3",
                "tokens": ["authentication", "golang", "impossible"]
            },
            {
                "id": "4",
                "tokens": ["network", "tcp", "ftp", "monitor", "reliability", "cable", "ethernet", "content", "network",
                           "router", "wifi", "cable", "ethernet", "socket", "authentication"]
            },
            {
                "id": "5",
                "tokens": ["python", "topic", "modelling", "module"]
            }
        ]
        tagger = LDATagger(model_path=config("app.model_path"), num_topics=config("app.max_topics"))
        documents_response = DocumentsResponse(documents_response_map)
        docs_tokens_map = documents_response.to_docs_tokens_map()
        tagger.build_topics(docs_tokens_map.values())


if __name__ == '__main__':
    unittest.main()
