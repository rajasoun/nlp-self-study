from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.httpserver import HTTPServer

from similarity.service import SimilarityService, ResourceSimilarityHandler
from similarity.service.similarity_handler import SimilarityHandler
from summary.service import SummaryHandler
from tagger.service import DocumentsHandler, ContentStoreService, DocumentProcessor, DocumentHandler
from tagger.config import load, config
from trinity import Logger
from web import VersionHandler
from web import ConfigHandler
from web import StatusHandler


logger = Logger.get_logger("TrinityApp")


class TrinityApp(Application):
    def __init__(self, config_file):
        self.config_file = config_file
        load(config_file)

        content_store_service = ContentStoreService()
        handlers = [
            ('/tagger/document', DocumentHandler, {"content_store_service": content_store_service,
                                                   "document_processor": DocumentProcessor(content_store_service)},),
            ('/tagger/documents', DocumentsHandler, {"content_store_service": content_store_service,
                                                     "processor": DocumentProcessor(content_store_service)},),
            ('/summary/document/_summarize', SummaryHandler),
            ('/summary/document/check_summarizability', SummaryHandler),
            ('/trinity/diagnostics/humans.txt', VersionHandler),
            ('/trinity/diagnostics/config.txt', ConfigHandler),
            ('/trinity/diagnostics/status.txt', StatusHandler),
            ('/similarity/documents', SimilarityHandler, {"similarity_service": SimilarityService(0.6)}),
            ('/similarity/resources', ResourceSimilarityHandler, {"similarity_threshold": 0.25})
        ]
        Application.__init__(self, handlers)

    def start(self):
        logger.info("Starting Trinity with config at %s with %s sub processes." % (
            self.config_file, config("app.process_count")))
        logger.info("Listening to requests on port %s" % config("app.port"))
        server = HTTPServer(self)
        server.bind(config("app.port"))
        server.start(int(config("app.process_count")))
        IOLoop.instance().start()


if __name__ == '__main__':
    import os

    config_file_path = os.path.join(os.path.dirname(__file__), "../config/sample.yml")
    TrinityApp(config_file_path).start()
