from unittest import TestCase
from tagger.service.contracts import DocumentsResponse


class TestDocumentResponse(TestCase):
    def test_shouldConvertListOfDocumentsJsonToDocumentTokensMap(self):
        documents_tokens_list = [
            {
                "id": "1",
                "tokens": ["network", "tcp", "udp"]
            },
            {
                "id": "2",
                "tokens": ["router", "switch", "cable"]
            }
        ]
        expected_doc_tokens_map = {
            "1": ["network", "tcp", "udp"],
            "2": ["router", "switch", "cable"]
        }
        document_response = DocumentsResponse(documents_tokens_list)
        actual_doc_tokens_map = document_response.to_docs_tokens_map()

        self.assertEquals(actual_doc_tokens_map,expected_doc_tokens_map)

