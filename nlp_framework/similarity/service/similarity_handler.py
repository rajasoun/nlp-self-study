import json

import requests
from tornado.web import RequestHandler
from trinity import Logger
from trinity.contracts import Response
from util import Unblock

logger = Logger.get_logger("SimilarityHandler")


class SimilarityHandler(RequestHandler):
    def initialize(self, similarity_service):
        self.similarity_service = similarity_service

    @Unblock()
    def post(self):
        logger.info("Request Received to calculate similarity between posts")

        parameters = json.loads(self.request.body)
        HEADERS = {'Content-Type': 'application/json'}

        try:
            similarity_map = self.similarity_service.find_similarity_across(parameters["documents"])
        except Exception as e:
            logger.exception("Error while computing similarity!")
            requests.post(parameters["callback_url"], data=Response(status="failure", message=e.message).to_json(),
                          headers=HEADERS)
        else:
            requests.post(parameters["callback_url"], data=(json.dumps(similarity_map)), headers=HEADERS)
