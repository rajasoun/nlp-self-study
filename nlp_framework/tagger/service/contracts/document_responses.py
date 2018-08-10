from collections import defaultdict


class DocumentsResponse:
    def __init__(self, document_map):
        self.document_map = document_map

    def to_docs_tokens_map(self):
        docs_tokens_map = defaultdict(list)
        for doc in self.document_map:
            if (doc):
                docs_tokens_map[doc["id"]] = doc["tokens"]
        return docs_tokens_map

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class DocumentResponse:
    def __init__(self, document_tokens_response):
        self.document_tokens_response = document_tokens_response

    def tokens(self):
        return self.document_tokens_response["tokens"]

    def document_id(self):
        return self.document_tokens_response["id"]

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
