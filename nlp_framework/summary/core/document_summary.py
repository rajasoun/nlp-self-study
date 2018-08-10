import json


class DocumentSummary:
    def __init__(self, doc_id, summary_sentences):
        self.doc_id = doc_id
        self.summary_sentences = summary_sentences

    def to_json(self):
        return json.dumps({
            "documentId": self.doc_id,
            "summary": self.summary_sentences,
            "status": "success"
        }, ensure_ascii=True, encoding="ascii")

    def __eq__(self, other):
        if isinstance(other, DocumentSummary):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
