import json

import os.path as os_path
import time
from tests.web.integration_test_case import IntegrationTestCase


class SummaryIntegrationTest(IntegrationTestCase):
    def setUp(self):
        super(SummaryIntegrationTest, self).setUp()
        self.text = """
        This is a random piece of text. It does not matter what is the content of this text block. Making sure that there is some content for ths summarization to figure out something
        """
        self.summary_request = {
            "documentId": "1",
            "extractedText": self.text,
            "callback": "http://localhost:9001/pipeline/summarized_document",
            "compressionRatio": "10"
        }
        self.ok_status_response = "{'status': 'ok'}"

    def test_should_create_summary_for_document(self):
        server = self.stub_http_server
        summary_response = {"documentId": "1", "summary": ["does not matter; This is a "
        ]}
        server.response_when(method="POST", path="/pipeline/summarized_document",
                             response=self.ok_status_response, responseType="application/json",
                             body=json.dumps(summary_response, ensure_ascii=True, encoding="ascii"))
        self.fetch("/summary/document/_summarize", method="PUT", body=json.dumps(self.summary_request))
        time.sleep(4)
        self.assertTrue(server.request_received("POST", "/pipeline/summarized_document"))
        stub_server_response = server.request_body_received_for("POST", "/pipeline/summarized_document")
        request_map = json.loads(stub_server_response)
        self.assertTrue(request_map.has_key("summary"))
        self.assertEqual(request_map["documentId"], summary_response["documentId"])

    def test_should_check_summarizability(self):
        summary_response = {"documentId": "1", "summarizability": True}
        response = self.fetch("/summary/document/check_summarizability", method="POST",
                              body=json.dumps(self.summary_request))
        request_map = json.loads(response.body)
        self.assertTrue(request_map.has_key("summarizability"))
        self.assertEqual(request_map["documentId"], summary_response["documentId"])