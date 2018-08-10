import json

import requests

from summary.core import Document
from summary.core import Summarizer
from trinity import Logger
from util import Unblock, Post
from util.tornado.web import MethodDispatcher

logger = Logger.get_logger("SummaryHandler")


class SummaryHandler(MethodDispatcher):
    @Unblock()
    def put(self):
        request_body = self.request.body
        logger.debug("Request received for summarisation; Request body: %s" % request_body[0:20])
        parameters = json.loads(request_body)

        callback_url = parameters["callback"]
        document_id = parameters["documentId"]
        extracted_text = parameters["extractedText"]
        compression_ratio = int(parameters["compressionRatio"])
        summarizer = Summarizer(compression_ratio=compression_ratio)
        document = Document(doc_id=document_id, text=extracted_text, summarizer=summarizer)

        try:
            logger.info("Generating Summary for document %s" % document_id)
            document_summary = document.summary()
        except Exception as e:
            logger.error("Error while generating summary for document %s" % document_id, e)
            requests.post(callback_url,
                          data=json.dumps({"status": "failure", "message": e.message, "documentId": document_id}),
                          headers={'Content-Type': 'application/json'})
        else:
            logger.info(
                "Summarisation completed for document %s. Updating to callback %s and sample summary %s" % (document_id, callback_url, document_summary.to_json()[0:20]))
            requests.post(callback_url, data=(document_summary.to_json()), headers={'Content-Type': 'application/json'})

    @Post()
    def check_summarizability(self):
        request_body = self.request.body
        logger.debug("Request received for checking summarizability; Request body: %s" % request_body[0:20])
        parameters = json.loads(request_body)

        document_id = parameters["documentId"]
        extracted_text = parameters["extractedText"]
        compression_ratio = int(parameters["compressionRatio"])
        summarizer = Summarizer(compression_ratio=compression_ratio)
        document = Document(doc_id=document_id, text=extracted_text, summarizer=summarizer)
        logger.info("Checking summarizability for %s" % document_id)
        summarizability = document.is_summarizable()
        logger.info("Summarizability for %s is %s" % (document_id, str(summarizability)))
        response = {
            "documentId": document_id,
            "summarizability": summarizability,
        }
        self.write(json.dumps(response))
        self.set_header("Content-Type", "application/json")