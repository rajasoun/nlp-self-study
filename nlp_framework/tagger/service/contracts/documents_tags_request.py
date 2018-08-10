import json


class DocumentsTagsRequest:
    def __init__(self, docs_tags_map):
        self.document_topics_map = docs_tags_map

    def to_json(self):
        json_response = []
        for doc_id, tags in self.document_topics_map.iteritems():
            doc_tags = {
                "id": doc_id,
                "tags": tags
            }
            json_response.append(doc_tags)
        return json.dumps(json_response)


class DocumentTagsRequest:
    def __init__(self, document_id, tags):
        self.tags = tags
        self.document_id = document_id

    def to_json(self):
        doc_tags = {
            "id": self.document_id,
            "tags": self.tags
        }
        return json.dumps(doc_tags)
