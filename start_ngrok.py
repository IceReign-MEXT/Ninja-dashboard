#!/usr/bin/env python

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
from pyngrok import ngrok

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Hello"
        self.send_response(200)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

logging.basicConfig(level=logging.INFO)

# Start ngrok tunnel
ngrok.set_auth_token("30dxkFANa3LoR0RV57mBFSs6Ndz_47MGq6BqgwQehk22KgeWz")
public_url = ngrok.connect(5000)
logging.info(f"Ngrok tunnel created: {public_url}")

# Start HTTP server
server = HTTPServer(("0.0.0.0", 5000), HelloHandler)
try:
    logging.info("Starting server. Press Ctrl+C to stop.")
    server.serve_forever()
except KeyboardInterrupt:
    logging.info("Shutting down server...")
    server.server_close()
    ngrok.disconnect(public_url)
    logging.info("Server stopped cleanly.")
