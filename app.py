#!/usr/bin/env python3
"""Health-serving HTTP service for the inbox API.

Runs with the standard library only, no pip install:

    python3 app.py

The database check is driven by the DB_UP environment variable so a
reviewer can simulate an outage without a real database:

    DB_UP=false python3 app.py
"""

import http.server
import os
import socketserver
import sys
import time

PORT = int(os.environ.get("PORT", "8080"))


def check_database():
    """Report whether the database is reachable.

    In production this opens a connection and runs SELECT 1. Here the
    result is driven by DB_UP so the endpoint can be exercised offline.
    """
    return os.environ.get("DB_UP", "true").lower() != "false"


class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/livez":
            self._respond(200, "ok\n")
        elif self.path == "/healthz":
            if check_database():
                self._respond(200, "ok\n")
            else:
                self._respond(503, "database unreachable\n")
        else:
            self._respond(404, "not found\n")

    def _respond(self, code, body):
        payload = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


def warm_up():
    """Load the voice models before serving. Takes a few seconds in production."""
    print("loading voice models, this takes a few seconds", flush=True)
    time.sleep(2)
    print("voice models loaded", flush=True)


def main():
    warm_up()
    with Server(("", PORT), HealthHandler) as httpd:
        print("listening on port %d" % PORT, flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
