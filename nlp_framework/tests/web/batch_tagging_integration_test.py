import json
import shutil
import unittest

import os
import os.path as os_path
from tests.web import StubHTTPServer
from tornado.testing import AsyncHTTPTestCase
from web import TrinityApp
from tagger.config import load, config


class BatchTaggingIntegrationTest(AsyncHTTPTestCase):
    config_path = os_path.join(os_path.abspath(os_path.dirname(__file__)), "config.yml")
    stub_http_server = None
    test_model_path = os_path.join(os_path.dirname(os_path.abspath(__file__)), "sample_test_model")
    document_response = [
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
    id_list = json.dumps({"documentIds": ["1", "2", "3", "4", "5"]})

    @classmethod
    def setUpClass(cls):
        cls.stub_http_server = StubHTTPServer(1111)
        cls.stub_http_server.start()
        load(cls.config_path)

    @classmethod
    def tearDownClass(cls):
        cls.stub_http_server.stop()

    def setUp(self):
        super(BatchTaggingIntegrationTest, self).setUp()
        self.stub_http_server.reset()

    def get_app(self):
        return TrinityApp(self.config_path)


    def test_shouldCreateModelWhenNoModelFound(self):
        server = self.stub_http_server
        self.id_list = json.dumps({"documentIds": ["1", "2", "3", "4", "5"]})
        self.clear_model(config("app.model_path"))

        server.response_when(method="GET", path="/documents/tokens", body=self.id_list,
                             response=json.dumps(self.document_response), responseType="application/json")

        response = self.fetch("/tagger/documents", method="POST", body=self.id_list)

        self.assertTrue(server.request_received(method="GET", path="/documents/tokens", body=self.id_list))
        self.assertTrue(server.request_received(method="POST", path="/documents/logical_topics"))
        self.assertTrue(os.path.exists(os.path.join(config("app.model_path"), "lda.model")))
        self.assertTrue(os.path.exists(os.path.join(config("app.model_path"), "tokens.dict")))

        self.assertEqual(200, response.code)
        self.assertEqual('success', json.loads(response.body)["status"])

    def test_shouldSendTopicToTokensAssociationToContentStore(self):
        server = self.stub_http_server
        self.id_list = json.dumps({"documentIds": ["1", "2", "3", "4", "5"]})
        self.clear_model(config("app.model_path"))

        server.response_when(method="GET", path="/documents/tokens", body=self.id_list,
                             response=json.dumps(self.document_response), responseType="application/json")

        response = self.fetch("/tagger/documents", method="POST", body=self.id_list)

        self.assertTrue(server.request_received(method="GET", path="/documents/tokens", body=self.id_list))
        self.assertTrue(server.request_received(method="POST", path="/documents/logical_topics"))

        self.assertEqual(200, response.code)
        self.assertEqual('success', json.loads(response.body)["status"])

    def test_shouldSendfailureResponseWhenTagDocumentsPostFails(self):
        server = self.stub_http_server
        self.id_list = json.dumps({"documentIds": ["1", "2", "3", "4", "5"]})
        self.clear_model(config("app.model_path"))

        server.response_when(method="GET", path="/documents/tokens", body=self.id_list,
                             response=json.dumps(self.document_response), responseType="application/json")
        server.response_when(method="POST", path="/documents/logical_topics", body=self.id_list,
                             response="[]", responseType="application/json",
                             status_code=500)

        response = self.fetch("/tagger/documents", method="POST", body=self.id_list)

        self.assertTrue(server.request_received(method="GET", path="/documents/tokens", body=self.id_list))
        self.assertTrue(server.request_received(method="POST", path="/documents/logical_topics"))
        self.assertFalse(server.request_received(method="POST", path="/topics/logical"))

        self.assertEqual(500, response.code)
        self.assertEqual('failure', json.loads(response.body)["status"])

    def test_shouldSendfailureResponseWhenDocumentsFetchFails(self):
        server = self.stub_http_server
        self.id_list = json.dumps({"documentIds": ["1", "2", "3", "4", "5"]})
        self.clear_model(config("app.model_path"))

        server.response_when(method="GET", path="/documents/tokens", body=self.id_list,
                             response="[]", responseType="application/json",
                             status_code=500)

        response = self.fetch("/tagger/documents", method="POST", body=self.id_list)

        self.assertTrue(server.request_received(method="GET", path="/documents/tokens", body=self.id_list))
        self.assertFalse(server.request_received(method="POST", path="/documents/logical_topics"))

        self.assertEqual(500, response.code)
        self.assertEqual('failure', json.loads(response.body)["status"])


    def clear_model(self, test_model_path):
        if os.path.exists(test_model_path):
            shutil.rmtree(test_model_path)


if __name__ == '__main__':
    unittest.main()
