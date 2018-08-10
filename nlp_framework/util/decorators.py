from functools import wraps, partial
from concurrent.futures import ThreadPoolExecutor
from trinity import Logger
from trinity.contracts import Response


class Unblock():
    def __init__(self):
        self.logger = Logger.get_logger("Unblock")
        self.executor = ThreadPoolExecutor(max_workers=100)
        self.logger.info("Created a ThreadPool")

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            handler = args[0]

            self.executor.submit(
                partial(f, *args, **kwargs)
            )
            self.logger.debug("Writing Async Response for %s" % handler.__class__)
            handler.write(Response(message="Successfully received request for %s" % handler.__class__).to_json())
            handler.set_header("Content-Type", "application/json")
            handler.finish()

        return wrapper


class Get():
    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            handler = args[0]
            if handler.request.method == "GET":
                f(*args, **kwargs)
            else:
                handler.send_error(status_code=405)

        return wrapper


class Post():
    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            handler = args[0]
            if handler.request.method == "POST":
                f(*args, **kwargs)
            else:
                handler.send_error(status_code=405)

        return wrapper


class Put():
    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            handler = args[0]
            if handler.request.method == "PUT":
                f(*args, **kwargs)
            else:
                handler.send_error(status_code=405)

        return wrapper


