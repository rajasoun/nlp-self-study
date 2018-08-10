from trinity import Logger

from tagger.core import LDATagger, TagGenerator
from tagger.config import config
from trinity.contracts import Response

logger = Logger.get_logger("DocumentProcessor")


class DocumentProcessor:
    def __init__(self, content_store_service):
        self.content_store_service = content_store_service

    def error_response(self, error_message):
        logger.error(error_message)
        return Response(status="failure", message=error_message)

    def process(self, docs_tokens_map, tagger_model_path):
        tagger = LDATagger(tagger_model_path, num_topics=config("app.max_topics"))

        tagger.build_or_update_model(docs_tokens_map.values())
        docs_topics_map = tagger.topics_for_documents(docs_tokens_map)
        topics_tokens_map = tagger.topics_to_tokens()
        docs_tags_map = TagGenerator(topics_tokens_map).generate_documents_tag_map(documents_tokens_map=docs_tokens_map,
                                                                                   documents_topics_map=docs_topics_map)

        try:
            self.content_store_service.post_documents_logical_topics_associations(docs_topics_map, topics_tokens_map)
        except Exception as e:
            document_topic_error_msg = "Error updating content store for documents with logical topics"
            logger.error(e)
            return self.error_response(document_topic_error_msg)

        try:
            self.content_store_service.post_documents_tags_associations(docs_tags_map)
        except Exception as e:
            docs_tags_error_msg = "Error updating content store with Documents' Tags"
            logger.error(e)
            return self.error_response(docs_tags_error_msg)

        return Response(status="success", message="Process Complete")

    def infer(self, document_response, tagger_model_path):
        tagger = LDATagger(tagger_model_path, num_topics=config("app.max_topics"))

        topics = tagger.topics_for_document(document_response.tokens())
        topics_tokens_map = tagger.topics_to_tokens()
        tags = TagGenerator(topics_tokens_map).generate_tags(topics=topics, tokens=document_response.tokens())

        try:
            self.content_store_service.post_document_logical_topics_association(document_response.document_id(), topics, topics_tokens_map)
        except Exception as e:
            document_topic_error_msg = "Error updating content store for document with logical topics"
            logger.error(e)
            return self.error_response(document_topic_error_msg)

        try:
            self.content_store_service.post_document_tags_association(document_response.document_id(), tags)
        except Exception as e:
            doc_tags_error_msg = "Error updating content store with Document Tags"
            logger.error(e)
            return self.error_response(doc_tags_error_msg)

        return Response(status="success", message="Process Complete")
