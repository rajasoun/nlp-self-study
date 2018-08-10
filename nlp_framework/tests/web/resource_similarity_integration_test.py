import json
import time

from tests.web.integration_test_case import IntegrationTestCase


class SimilarityIntegrationTest(IntegrationTestCase):
    ok_status_response = "{'status': 'ok'}"

    def test_should_find_similarity_between_resources(self):
        server = self.stub_http_server
        similarity_request = {
            "callback_url": "http://localhost:9001/pipeline/similarity",
            "resources": [
                {
                    "id": "sha1",
                    "title": {
                        "value": "this is a simple title",
                        "weight": 1
                    },
                    "description": {
                        "value": "This is a simple description"
                    },
                    "tags": {
                        "value": ["simple", "title", "description"],
                        "weight": 2
                    }
                }, {
                    "id": "sha2",
                    "title": {
                        "value": "post about batman",
                        "weight": 1
                    },
                    "description": {
                        "value": "Batman is awesome. A billionaire industrialist whose parents were killed by a mugger when he was eight years old. Traveling the world for several years to learn and experience the inner workings of the crimminal mind, and seeking the means to fight injustice, he later returns to Gotham and at night becomes the Batman, Gotham City's shadowy vigilante protector."
                    },
                    "tags": {
                        "value": ["batman", "bruce"],
                    }
                },
                {
                    "id": "sha3",
                    "name": {
                        "value": "Batman Fan Group",
                        "weight": 1
                    },
                    "description": {
                        "value": "A billionaire industrialist whose parents were killed by a mugger when he was eight years old. Traveling the world for several years to learn and experience the inner workings of the crimminal mind, and seeking the means to fight injustice, he later returns to Gotham and at night becomes the Batman, Gotham City's shadowy vigilante protector",
                        "weight": 10
                    },
                    "tags": {
                        "value": ["batman", "fan"],
                        "weight": 3
                    },
                    "type": {
                        "value": "group"
                    }
                }
            ]

        }

        similarity_callback_response = {
            "sha2": ["sha3"],
            "sha3": ["sha2"]
        }

        server.response_when(method="POST", path="/pipeline/similarity", body=json.dumps(similarity_callback_response),
                             response=self.ok_status_response, responseType="application/json")

        self.fetch("/similarity/resources", method="POST", body=json.dumps(similarity_request))
        time.sleep(5)
        self.assertTrue(server.request_received("POST", "/pipeline/similarity"))
        request_body = json.loads(server.request_body_received_for("POST", "/pipeline/similarity"))
        self.assertEquals(similarity_callback_response, request_body)
