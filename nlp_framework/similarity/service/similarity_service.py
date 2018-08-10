from collections import defaultdict
from similarity.core import AuthoredDocument
from trinity import Logger

logger = Logger.get_logger("SimilarityService")


class SimilarityService():
    def __init__(self, similarity_threshold):
        self.similarity_threshold = similarity_threshold

    def find_similarity_across(self, input_documents_map):
        logger.info("Calculating Similarity for documents")
        similarity_map = defaultdict(list)
        for document_id, document in input_documents_map.iteritems():
            similarity_map[document_id] = []
            authored_document = AuthoredDocument(document_id, document)
            for other_document_id, other_document in input_documents_map.iteritems():
                if document_id == other_document_id:
                    continue

                other_authored_document = AuthoredDocument(other_document_id, other_document)
                similarity_score = authored_document.similarity_score(other_authored_document)
                logger.info("Similarity Score between document %s and %s is %f" % (
                    document_id, other_document_id, similarity_score))
                if similarity_score > self.similarity_threshold:
                    similarity_map[document_id].append(other_document_id)
        return similarity_map