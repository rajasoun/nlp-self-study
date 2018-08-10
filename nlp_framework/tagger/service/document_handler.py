import httplib
import json
import os
from tagger.config import config
from tagger.core import LDATagger
from tornado.web import RequestHandler
from trinity import Logger
from trinity.contracts import Response

logger = Logger.get_logger("DocumentsHandler")


class DocumentHandler(RequestHandler):
    def initialize(self, document_processor, content_store_service):
        self.document_processor = document_processor
        self.content_store_service = content_store_service

    def post(self):

        document_id = json.loads(self.request.body)["documentId"]
        logger.info("Request to infer topics for document %s received" % document_id)

        try:
            document_response = self.content_store_service.fetch_document(document_id)
        except Exception as e:
            document_fetch_error = "unable to fetch Document for Tagging"
            logger.info(e)
            logger.error("%s for Id %s" % (document_fetch_error, document_id))
            return self.error_response(document_fetch_error)

        model_path = config("app.model_path", LDATagger.DEFAULT_MODEL_PATH)

        logger.info("Model Path: %s" % (model_path))
        logger.info("Inferring topics and tags for %s" % document_id)

        result = self.document_processor.infer(document_response, os.path.abspath(model_path))

        logger.info("Topics and tags for %s successfully generated" % document_id)

        if not result.is_success():
            self.set_status(httplib.INTERNAL_SERVER_ERROR)

        self.write(result.to_json())
        self.set_header("Content-Type", "application/json")

    def error_response(self, error_msg):
        self.set_status(httplib.INTERNAL_SERVER_ERROR)
        error_response = Response(status="failure", message=error_msg)
        self.write(error_response.to_json())
        self.set_header("Content-Type", "application/json")
