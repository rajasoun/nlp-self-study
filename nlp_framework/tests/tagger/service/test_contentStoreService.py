import json
from unittest import TestCase

from os import path as os_path
from tagger.config import load
from tagger.service import ContentStoreService
from tagger.service.contracts import DocumentsResponse, DocumentTopicsMixturesRequest, TopicTokensMixturesRequest, DocumentsTagsRequest
from tagger.service.contracts.document_topics_mixture_requests import DocumentTopicsMixtureRequest
from tagger.service.contracts.documents_tags_request import DocumentTagsRequest
from tests.web.stub_http_server import StubHTTPServer


class TestContentStoreService(TestCase):
    stub_http_server = None
    config_path = os_path.join(os_path.abspath(os_path.dirname(__file__)), "../../web/config.yml")

    @classmethod
    def setUpClass(cls):
        cls.stub_http_server = StubHTTPServer(1111)
        cls.stub_http_server.start()
        load(cls.config_path)

    @classmethod
    def tearDownClass(cls):
        cls.stub_http_server.stop()

    def setUp(self):
        self.document_request = {"documentIds": ["sha1", "sha2", "sha3", "sha4", "sha5"]}
        self.document_response = [
            {
                "id": "sha1",
                "tokens": ["content", "network", "router", "wifi", "cable", "ethernet", "socket", "authentication",
                           "content",
                           "network", "router", "wifi", "cable", "ethernet", "socket", "authentication"]
            },
            {
                "id": "sha2",
                "tokens": ["java", "golang", "cool", "awesome"]
            },
            {
                "id": "sha3",
                "tokens": ["authentication", "golang", "impossible"]
            },
            {
                "id": "sha4",
                "tokens": ["network", "tcp", "ftp", "monitor", "reliability", "cable", "ethernet", "content", "network",
                           "router", "wifi", "cable", "ethernet", "socket", "authentication"]
            },
            {
                "id": "sha5",
                "tokens": ["python", "topic", "modelling", "module"]
            }
        ]
        #self.document_logical_topics_map = {
        #    "sha1": [("0", 0.92), ("1", 0.08)],
        #    "sha2": [("2", 0.92), ("1", 0.08)],
        #    "sha3": [("2", 0.92), ("1", 0.08)],
        #    "sha4": [("2", 0.92), ("1", 0.08)],
        #    "sha5": [("1", 0.92), ("3", 0.08)]
        #}
        self.document_logical_topics = ("sha1", [("0", 0.92), ("1", 0.08)])
        #self.logical_topics_tokens_map = {
        #    "0": {"network": 0.002, "tcp": 0.34, "ethernet": 0.45},
        #    "1": {"udp": 0.02, "cable": 0.3, "router": 0.4},
        #    "2": {"python": 0.2, "java": 0.34, "clojure": 0.45},
        #    "3": {"network": 0.002, "tcp": 0.34, "ethernet": 0.5}
        #}
        self.documents_tags_map = {
            "sha1": ["network", "router", "tcp"],
            "sha2": ["python", "java"],
            "sha3": ["router", "ethernet"],
            "sha4": ["cable", "udp"],
            "sha5": ["python", "golang"]
        }

        self.document_logical_topics_map = {
            "sha1": [("0", 0.92), ("1", 0.08)],
            "sha2": [("2", 0.92), ("1", 0.08)],
            "sha3": [("2", 0.92), ("1", 0.08)],
            "sha4": [("2", 0.92), ("1", 0.08)],
            "sha5": [("1", 0.92), ("3", 0.08)]
        }

        self.logical_topics_tokens_map = {
            "0": {"network": 0.002, "tcp": 0.34, "ethernet": 0.45},
            "1": {"udp": 0.02, "cable": 0.3, "router": 0.4},
            "2": {"python": 0.2, "java": 0.34, "clojure": 0.45},
            "3": {"network": 0.002, "tcp": 0.34, "ethernet": 0.5}
        }
        self.content_store_service = ContentStoreService()
        self.stub_http_server.reset()

    def test_should_get_tokenised_documents_given_list_of_ids(self):
        server = self.stub_http_server
        server.response_when(method="GET", path="/documents/tokens", body=json.dumps(self.document_request),
                             response=json.dumps(self.document_response), responseType="application/json")

        expected_documents_response = DocumentsResponse(self.document_response)
        actual_response = self.content_store_service.fetch_documents(json.dumps(self.document_request))

        self.assertTrue(
            server.request_received(method="GET", path="/documents/tokens", body=json.dumps(self.document_request)))
        self.assertEquals(actual_response, expected_documents_response)

    def test_should_raise_exception_when_failure_to_fetch_tokenised_documents(self):
        server = self.stub_http_server
        server.response_when(method="GET", path="/documents/tokens", body=json.dumps(self.document_request),
                             response="Internal Server Error", responseType="application/json", status_code=500)

        with self.assertRaises(Exception) as exception:
            self.content_store_service.fetch_documents(json.dumps(self.document_request))

        self.assertTrue(
            server.request_received(method="GET", path="/documents/tokens", body=json.dumps(self.document_request)))
        self.assertEquals(exception.exception.message, ContentStoreService.STATUS_FAILED)

    def test_should_post_documents_topics_association(self):
        server = self.stub_http_server
        document_logical_topics_request = DocumentTopicsMixturesRequest(self.document_logical_topics_map, self.logical_topics_tokens_map)
        server.response_when(method="POST", path="/documents/logical_topics",
                             body=document_logical_topics_request.to_json(),
                             response="{'status' : 'success'}", responseType="application/json")
        self.content_store_service.post_documents_logical_topics_associations(self.document_logical_topics_map, self.logical_topics_tokens_map)

        self.assertTrue(
            server.request_received(method="POST", path="/documents/logical_topics",
                                    body=document_logical_topics_request.to_json()))

    def test_should_post_document_topics_association(self):
        server = self.stub_http_server
        document_logical_topics_request = DocumentTopicsMixtureRequest(document_id=self.document_logical_topics[0],
                                                                       topics=self.document_logical_topics[1],
                                                                       topics_tokens_map=self.logical_topics_tokens_map)
        server.response_when(method="POST", path="/document/logical_topics",
                             body=document_logical_topics_request.to_json(),
                             response="{'status' : 'success'}", responseType="application/json")
        self.content_store_service.post_document_logical_topics_association(document_id=self.document_logical_topics[0],
                                                                            topics=self.document_logical_topics[1],
                                                                            topics_tokens_map=self.logical_topics_tokens_map)

        self.assertTrue(
            server.request_received(method="POST", path="/document/logical_topics",
                                    body=document_logical_topics_request.to_json()))

    def test_should_raise_exception_when_failure_to_post_documents_logical_topics(self):
        server = self.stub_http_server
        document_logical_topics_request = DocumentTopicsMixturesRequest(self.document_logical_topics_map, self.logical_topics_tokens_map)
        server.response_when(method="POST", path="/documents/logical_topics",
                             body=document_logical_topics_request.to_json(),
                             response="Internal Server Error", responseType="application/json", status_code=500)

        with self.assertRaises(Exception) as exception:
            self.content_store_service.post_documents_logical_topics_associations(
                self.document_logical_topics_map,
                topics_tokens_map=self.logical_topics_tokens_map)

        self.assertTrue(
            server.request_received(method="POST", path="/documents/logical_topics",
                                    body=document_logical_topics_request.to_json()))
        self.assertEquals(exception.exception.message, ContentStoreService.STATUS_FAILED)

    def test_should_raise_exception_when_failure_to_post_document_logical_topics(self):
        server = self.stub_http_server
        document_logical_topics_request = DocumentTopicsMixtureRequest(document_id=self.document_logical_topics[0],
                                                                       topics=self.document_logical_topics[1],
                                                                       topics_tokens_map=self.logical_topics_tokens_map)
        server.response_when(method="POST", path="/document/logical_topics",
                             body=document_logical_topics_request.to_json(),
                             response="Internal Server Error", responseType="application/json", status_code=500)

        with self.assertRaises(Exception) as exception:
            self.content_store_service.post_document_logical_topics_association(
                document_id=self.document_logical_topics[0],
                topics=self.document_logical_topics[1],
                topics_tokens_map=self.logical_topics_tokens_map)

        self.assertTrue(
            server.request_received(method="POST", path="/document/logical_topics",
                                    body=document_logical_topics_request.to_json()))
        self.assertEquals(exception.exception.message, ContentStoreService.STATUS_FAILED)

    def test_should_post_documents_tags_association(self):
        server = self.stub_http_server
        documents_tags_request = DocumentsTagsRequest(self.documents_tags_map)
        server.response_when(method="POST", path="/documents/tags",
                             body=documents_tags_request.to_json(),
                             response="{'status' : 'success'}", responseType="application/json")
        self.content_store_service.post_documents_tags_associations(self.documents_tags_map)

        self.assertTrue(server.request_received(method="POST", path="/documents/tags",
                                                body=documents_tags_request.to_json()))

    def test_should_raise_exception_when_failure_to_documents_tags_association(self):
        server = self.stub_http_server
        documents_tags_request = DocumentsTagsRequest(self.documents_tags_map)
        server.response_when(method="POST", path="/documents/tags",
                             body=documents_tags_request.to_json(),
                             response="Internal Server Error", responseType="application/json", status_code=500)
        with self.assertRaises(Exception) as exception:
            self.content_store_service.post_documents_tags_associations(self.documents_tags_map)

        self.assertTrue(server.request_received(method="POST", path="/documents/tags",
                                                body=documents_tags_request.to_json()))
        self.assertEquals(exception.exception.message, ContentStoreService.STATUS_FAILED)

    def test_should_post_document_tags_association(self):
        server = self.stub_http_server
        document_id = "sha1"
        tags = ["tag1", "tag2", "tag3"]
        document_tags_request = DocumentTagsRequest(document_id=document_id, tags=tags)
        server.response_when(method="POST", path="/document/tags",
                             body=document_tags_request.to_json(),
                             response="{'status' : 'success'}", responseType="application/json")
        self.content_store_service.post_document_tags_association(document_id=document_id, tags=tags)

        self.assertTrue(server.request_received(method="POST", path="/document/tags",
                                                body=document_tags_request.to_json()))

    def test_should_raise_exception_when_failure_to_document_tags_association(self):
        server = self.stub_http_server
        document_id = "sha1"
        tags = ["tag1", "tag2", "tag3"]
        document_tags_request = DocumentTagsRequest(document_id=document_id, tags=tags)
        server.response_when(method="POST", path="/document/tags",
                             body=document_tags_request.to_json(),
                             response="Internal Server Error", responseType="application/json", status_code=500)
        with self.assertRaises(Exception) as exception:
            self.content_store_service.post_document_tags_association(document_id=document_id, tags=tags)

        self.assertTrue(server.request_received(method="POST", path="/document/tags",
                                                body=document_tags_request.to_json()))
        self.assertEquals(exception.exception.message, ContentStoreService.STATUS_FAILED)

