import os
from tornado.web import RequestHandler

class VersionHandler(RequestHandler):
    def get(self):
        self.set_header("Cache-control", "no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0")
        filename = os.getcwd() + "/humans.txt"
        with open(filename) as f:
            self.write(f.read())
