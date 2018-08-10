import json
import os
import os.path as os_path
from tests.web.integration_test_case import IntegrationTestCase
from trinity import Logger

logger = Logger.get_logger("TestSimilarityExperiment")


class TestSimilarityExperiment(IntegrationTestCase):
    ok_status_response = "{'status': 'ok'}"

    def wait(self, condition=None, timeout=None):
        super(TestSimilarityExperiment, self).wait(condition=None, timeout=60)

    def test_should_find_smililarity_between_blogs(self):
        server = self.stub_http_server

        similarity_request = {
            "callback_url": "http://localhost:9001/pipeline/similarity",
            "documents": {}
        }

        blogs_dir = os_path.join(os_path.abspath(os_path.dirname(__file__)), "blogs")
        blogs = os.listdir(blogs_dir)
        blogs.remove(".gitignore")
        if (len(blogs) == 0):
            pass
            return

        for blog_name in blogs:
            blog_file = open(os_path.join(blogs_dir, blog_name), "r")

            similarity_request["documents"][blog_name.replace(" ", "_")] = {
                "title": blog_name,
                "body": json.dumps(blog_file.read()),
                "tags": []
            }

            blog_file.close()

        logger.info(json.dumps(similarity_request))
        server.response_when(method="POST", path="/pipeline/similarity",
                             response=self.ok_status_response, responseType="application/json")

        self.fetch("/similarity/documents", method="PUT", body=json.dumps(similarity_request))

        request_body = server.request_body_received_for("POST", "/pipeline/similarity")
        logger.info(request_body)
