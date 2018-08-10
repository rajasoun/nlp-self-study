from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
import requests


class StubRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        content = self._content()
        self.server.log_request('GET', self.path, content)
        self._send_server_response(('GET', self.path, content))

    def do_POST(self):
        content = self._content()
        self.server.log_request('POST', self.path, content)
        self._send_server_response(('POST', self.path, content))

    def _content(self):
        try:
            length = int(self.headers.getheader('content-length'))
        except (TypeError, ValueError):
            return ""
        else:
            return self.rfile.read(length)

    def _send_server_response(self, request):
        content_to_send = self.server.content(request)

        self.send_response(content_to_send[2])

        for (key, value) in self.server.header_dict().items():
            self.send_header(key, value)

        self.send_header("content-type", content_to_send[1])
        self.end_headers()

        self.wfile.write(content_to_send[0])


class StubHTTPServer(HTTPServer):
    def __init__(self, port_number=0):
        address = ('127.0.0.1', port_number)
        HTTPServer.__init__(self, address, StubRequestHandler)
        self.start()
        self._requests = []
        self._responses = []
        self._header_dict = {}
        self._status_code = 200
        self._content = ["ok", "text/plain", 200]

    def start(self):
        server_thread = threading.Thread(target=self.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def stop(self):
        self.shutdown()
        self.server_close()
        self.verify_shutdown()

    def log_request(self, request_type, path, content):
        self._requests.append((request_type, path, content))

    def requests(self):
        return self._requests

    def set_response(self, header_dict, status_code, content):
        self._header_dict = header_dict
        self._status_code = status_code
        self._content = content

    def header_dict(self):
        return self._header_dict

    def status_code(self):
        return self._status_code

    def content(self, request):
        for response in self._responses:
            if request[0] == response[0] and request[1] == response[1] and (
                        response[5] != 200 or self.is_empty(request[2]) or request[2] == response[2]):
                return [response[3], response[4], response[5]]
        return self._content

    def request_received(self, method, path, body=None):
        for request in self._requests:
            if method == request[0] and path == request[1] and (body is None or body == request[2]):
                return True
        return False

    def request_body_received_for(self, method, path):
        for request in self._requests:
            if method == request[0] and path == request[1]:
                return request[2]
        return ""

    def response_when(self, method, path, response, responseType, body=None, status_code=200):
        self._responses.append((method, path, body, response, responseType, status_code))

    def is_empty(self, request_string):
        return (request_string is None) or request_string == ""

    def reset(self):
        self._requests = []
        self._responses = []

    def verify_shutdown(self):
        try:
            requests.get("http://127.0.0.1:%s/_shutdown" % str(self.server_port))
        except requests.ConnectionError:
            pass
