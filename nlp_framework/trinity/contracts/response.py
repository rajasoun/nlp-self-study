import json


class Response:
    SUCCESS = "success"
    SUCCESS_MESSAGE = "default success message"
    status = ""
    message = ""
    errors = []

    def __init__(self, status=SUCCESS, message=SUCCESS_MESSAGE, errors=[]):
        self.status = status
        self.message = message
        self.errors = errors

    def is_success(self):
        return self.status == self.SUCCESS

    def to_json(self):
        return json.dumps({
            "status": self.status,
            "message": self.message,
            "errors": self.errors,
        })

