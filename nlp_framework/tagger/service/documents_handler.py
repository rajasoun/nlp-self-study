import httplib

import os
from tagger.core import LDATagger
from trinity.contracts import Response
from tornado.web import RequestHandler
from tagger.config import config
from trinity import Logger

logger = Logger.get_logger("DocumentsHandler")


class DocumentsHandler(RequestHandler):
    def initialize(self, content_store_service, processor):
        self.content_store_service = content_store_service
        self.processor = processor

    def post(self):
        list_of_ids = self.request.body
        logger.info("Request to model topics for documents %s received" % str(list_of_ids))

        try:
            documents_response = self.content_store_service.fetch_documents(list_of_ids)
        except Exception as e:
            document_fetch_error = "unable to fetch Documents for Tagging"
            logger.info(e)
            logger.error("%s for Id %s" % (str(document_fetch_error), str(list_of_ids)))

            return self.error_response(document_fetch_error)

        model_path = config("app.model_path", LDATagger.DEFAULT_MODEL_PATH)
        logger.info("Model Path: %s" % (model_path))
        docs_tokens_map = documents_response.to_docs_tokens_map()
        result = self.processor.process(docs_tokens_map, os.path.abspath(model_path))

        if not result.is_success():
            self.set_status(httplib.INTERNAL_SERVER_ERROR)

        self.write(result.to_json())
        self.set_header("Content-Type", "application/json")

    def error_response(self, error_msg):
        self.set_status(httplib.INTERNAL_SERVER_ERROR)
        error_response = Response(status="failure", message=error_msg)
        self.write(error_response.to_json())
        self.set_header("Content-Type", "application/json")
