import json

import httplib
import requests
from tagger.config import config
from tagger.service.contracts import DocumentsResponse, DocumentTopicsMixturesRequest, DocumentsTagsRequest, \
    DocumentResponse
from tagger.service.contracts.document_topics_mixture_requests import DocumentTopicsMixtureRequest
from tagger.service.contracts.documents_tags_request import DocumentTagsRequest
from trinity import Logger

logger = Logger.get_logger("ContentStoreService")


class ContentStoreService:
    HEADERS = {'Content-Type': 'application/json'}
    CONNECTION_ERROR = "Connection Error While Fetching"
    STATUS_FAILED = "Failed. Status Not Ok"

    def fetch_documents(self, documents_request):
        get_docs_url = config("content_store.host") + config("content_store.get_docs")
        response = None
        try:
            logger.info("Fetching %s Documents to Tag from %s" % (documents_request, get_docs_url))
            response = requests.get(get_docs_url, data=documents_request, headers=self.HEADERS)
            if response.status_code is not httplib.OK:
                logger.error(response.text)
                raise Exception(self.STATUS_FAILED)
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception(self.CONNECTION_ERROR)
        logger.debug("Received Tokenised Documents for tagging. Server Response %s" % response.text)
        return DocumentsResponse(response.json())

    def fetch_document(self, document_id):
        get_doc_url = config("content_store.host") + config("content_store.get_doc") % document_id
        response = None
        try:
            logger.info("Fetching %s Document to Tag from %s" % (document_id, get_doc_url))
            response = requests.get(get_doc_url, headers=self.HEADERS)
            if response.status_code is not httplib.OK:
                logger.error(response.text)
                raise Exception(self.STATUS_FAILED)
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception(self.CONNECTION_ERROR)
        logger.info(
            "Received Tokenised Document for tagging with %s tokens." % len(json.loads(response.text)["tokens"]))
        logger.debug("Received Tokenised Document for tagging. Server Response %s" % response.text)
        return DocumentResponse(response.json())

    def post_documents_logical_topics_associations(self, docs_topics_map, topics_tokens_map):
        document_topics_mixtures = DocumentTopicsMixturesRequest(docs_topics_map, topics_tokens_map)
        post_documents_logical_topics_url = config("content_store.host") + config(
            "content_store.post_documents_logical_topics")
        response = None
        try:
            logger.info("Posting Documents tagged with Logical Topics to %s" % post_documents_logical_topics_url)
            response = requests.post(post_documents_logical_topics_url, data=document_topics_mixtures.to_json(),
                                     headers=self.HEADERS)
            if response.status_code is not httplib.OK:
                logger.error(response.text)
                raise Exception(self.STATUS_FAILED)
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception(self.CONNECTION_ERROR)
        logger.info("Successfully posted Logical Topics for Documents. Server Response: %s" % response.text)

    def post_document_logical_topics_association(self, document_id, topics, topics_tokens_map):
        document_topics_mixture = DocumentTopicsMixtureRequest(document_id=document_id, topics=topics,
                                                               topics_tokens_map=topics_tokens_map)
        post_document_logical_topics_url = config("content_store.host") + config(
            "content_store.post_document_logical_topics")
        response = None
        try:
            logger.info("Posting Document tagged with Logical Topics to %s" % post_document_logical_topics_url)
            response = requests.post(post_document_logical_topics_url, data=document_topics_mixture.to_json(),
                                     headers=self.HEADERS)
            if response.status_code is not httplib.OK:
                logger.error(response.text)
                raise Exception(self.STATUS_FAILED)
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception(self.CONNECTION_ERROR)
        logger.info("Successfully posted Logical Topics for Document %s. Server Response: %s" % (document_id,
                                                                                                 response.text))

    def post_documents_tags_associations(self, docs_tags_map):
        document_tags_mixtures = DocumentsTagsRequest(docs_tags_map)
        post_documents_tags_url = config("content_store.host") + config("content_store.post_documents_tags")
        response = None
        try:
            logger.info("Posting Document-Tags association to %s" % post_documents_tags_url)
            response = requests.post(post_documents_tags_url, data=document_tags_mixtures.to_json(),
                                     headers=self.HEADERS)
            if response.status_code is not httplib.OK:
                logger.error(response.text)
                raise Exception(self.STATUS_FAILED)
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception(self.CONNECTION_ERROR)
        logger.info("Successfully posted Document-Tags associations. Server Response: %s" % response.text)

    def post_document_tags_association(self, document_id, tags):
        document_tags_request = DocumentTagsRequest(document_id, tags)
        post_document_tags_url = config("content_store.host") + config("content_store.post_document_tags")
        response = None
        try:
            logger.info("Posting Document-Tags association to %s" % post_document_tags_url)
            response = requests.post(post_document_tags_url, data=document_tags_request.to_json(),
                                     headers=self.HEADERS)
            if response.status_code is not httplib.OK:
                logger.error(response.text)
                raise Exception(self.STATUS_FAILED)
        except requests.ConnectionError as e:
            logger.error(e)
            raise Exception(self.CONNECTION_ERROR)
        logger.info("Successfully posted Document-Tags association. Server Response: %s" % response.text)
