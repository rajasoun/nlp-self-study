import os.path as os_path

from tests.web import StubHTTPServer
from tornado.testing import AsyncHTTPTestCase
from web import TrinityApp


class IntegrationTestCase(AsyncHTTPTestCase):
    config_path = os_path.join(os_path.abspath(os_path.dirname(__file__)), "config.yml")
    stub_http_server = None

    @classmethod
    def setUpClass(cls):
        cls.stub_http_server = StubHTTPServer(9001)
        cls.stub_http_server.start()

    @classmethod
    def tearDownClass(cls):
        cls.stub_http_server.stop()

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.stub_http_server.reset()

    def get_app(self):
        return TrinityApp(self.config_path)
