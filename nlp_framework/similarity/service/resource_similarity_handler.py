import json

import requests
from similarity.service.resource_similarity_service import all_resources_similarity
from tornado.web import RequestHandler
from trinity import Logger
from trinity.contracts import Response
from util import Unblock

logger = Logger.get_logger("ResourceSimilarityHandler")


class ResourceSimilarityHandler(RequestHandler):
    def initialize(self, similarity_threshold):
        self.similarity_threshold = similarity_threshold

    @Unblock()
    def post(self):
        """
            Accepts a request with json as below:
            {
                "resources" : [resource1,resource2..]
                "callback_url": "callback url"
            }

            resource = {
                "id": sha123,
                "field1" : {
                    "value": bla,
                    "weight" : optional
                },
                "field2" : {
                    "value": bla bla,
                    "weight" : 2
                }
            }
        """
        logger.info("Request Received to calculate similarity between resources")

        parameters = json.loads(self.request.body)
        HEADERS = {'Content-Type': 'application/json'}

        callback_url = parameters["callback_url"]
        try:
            logger.info("Sample resource in request [%s]" % (parameters["resources"][0]))
            similarity_map = all_resources_similarity(parameters["resources"], self.similarity_threshold)
        except Exception as e:
            logger.exception("Error while computing similarity!")
            requests.post(callback_url, data=Response(status="failure", message=e.message).to_json(),
                          headers=HEADERS)
        else:
            logger.info("Similarity Calculation complete for resources, posting to [%s] with [%s]" % (
            callback_url, json.dumps(similarity_map)))
            requests.post(callback_url, data=(json.dumps(similarity_map)), headers=HEADERS)
