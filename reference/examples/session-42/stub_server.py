"""Loopback-only HTTP fixture for Session 42. Run: python3 stub_server.py"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get("X-API-Key") != "training-demo-only":
            status = 401
        elif self.path == "/ok":
            status = 200
        elif self.path == "/unavailable":
            status = 503
        elif self.path == "/slow":
            sleep(3)
            status = 200
        else:
            status = 404
        try:
            self.send_response(status)
            self.end_headers()
            self.wfile.write(f"status={status}\n".encode())
        except BrokenPipeError:
            pass  # The client intentionally closes /slow after its read timeout.


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
