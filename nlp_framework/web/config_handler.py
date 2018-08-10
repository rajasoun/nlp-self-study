import os
from tornado.web import RequestHandler
from tagger.config import fullConfigAsString

class ConfigHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.set_header("Cache-control", "no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0")
        self.write(fullConfigAsString())
