import json

import requests
from tagger.config import config
from tornado.web import RequestHandler


class StatusHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-control",
                        "no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0")
        self.write(allStatuses())


def allStatuses():
    dependencies = []
    dependencies.append(
        restStatus("ContentStore HTTP connection", config("content_store.host") + "/diagnostics/humans.txt"))
    return json.dumps({
        "dependencies": dependencies,
        "status": reduce(
            lambda current_status, dependency: "yellow" if dependency["status"] == "red" else current_status,
            dependencies, "green")
    })


def restStatus(name, url):
    result = {
        "status": "green",
        "name": name,
        "location": url
    }
    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except Exception as e:
        result["error"] = str(e)
        result["status"] = "red"
    return result
