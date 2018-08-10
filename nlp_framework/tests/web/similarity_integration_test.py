import json
from tests.web.integration_test_case import IntegrationTestCase


class SimilarityIntegrationTest(IntegrationTestCase):
    ok_status_response = "{'status': 'ok'}"

    def ignored_should_find_similarity_between_posts(self):
        server = self.stub_http_server
        similarity_request = {
            "callback_url": "http://localhost:9001/pipeline/similarity",
            "documents": {
                "sha1": {
                    "title": "this is a title",
                    "body": "this is my first blog, hence sucks",
                    "tags": []
                },

                "sha2": {
                    "title": "this is a another title blog",
                    "body": "this is my second blog, which is much better",
                    "tags": []
                },

                "sha3": {
                    "title": "a very mature title blog post ",
                    "body": "We are surrounded by objects in the real world. This is my better second blog",
                    "tags": []
                }
            }
        }

        similarity_callback_response = {
            "sha1": ["sha2", "sha3"],
            "sha2": ["sha1", "sha3"],
            "sha3": ["sha2", "sha1"]
        }

        server.response_when(method="POST", path="/pipeline/similarity", body=json.dumps(similarity_callback_response),
                             response=self.ok_status_response, responseType="application/json")

        self.fetch("/similarity/documents", method="POST", body=json.dumps(similarity_request))

        self.assertTrue(server.request_received("POST", "/pipeline/similarity"))
        request_body = server.request_body_received_for("POST", "/pipeline/similarity")
        request_map = json.loads(request_body)

        self.assertEqual(set(request_map["sha1"]), set(similarity_callback_response["sha1"]))
        self.assertEqual(set(request_map["sha2"]), set(similarity_callback_response["sha2"]))
        self.assertEqual(set(request_map["sha3"]), set(similarity_callback_response["sha3"]))


