#!/usr/bin/env python3
"""Local helper server for generating GeoGebra .ggb files via a browser.

Why: the ONLY reliable way to produce a valid .ggb is to let the real GeoGebra
engine build it and export it (getBase64). This server (a) serves the generator
page that loads that engine, and (b) receives the exported file from the browser
and writes it to disk — so you never have to pipe huge base64 blobs through the
agent's context.

What it does:
  GET  /generator.html   -> serves templates/generator.html (loads GeoGebra)
  GET  /<anything>       -> serves files from OUTPUT_DIR (for round-trip checks)
  POST /save?name=x.ggb  -> body is base64 of the .ggb; decodes and writes
                            OUTPUT_DIR/x.ggb

Usage:
    python3 scripts/ggb_server.py [OUTPUT_DIR] [PORT]
    # defaults: OUTPUT_DIR = current directory, PORT = 8777

Then open  http://localhost:PORT/generator.html  in a browser and drive the
GeoGebra applet via its JS API (see SKILL.md, Stage C).
"""
import base64
import http.server
import os
import socketserver
import sys
import urllib.parse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "templates", "generator.html"))

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8777
os.makedirs(OUT, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=OUT, **k)

    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/generator.html"):
            try:
                data = open(TEMPLATE, "rb").read()
            except Exception as e:  # noqa
                self.send_error(500, "generator.html not found: %s" % e)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(data)
            return
        return super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = q.get("name", ["out.ggb"])[0].replace("/", "_").replace("..", "")
        if not name.endswith(".ggb"):
            name += ".ggb"
        try:
            raw = base64.b64decode(body)
            with open(os.path.join(OUT, name), "wb") as f:
                f.write(raw)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(("OK %d bytes -> %s" % (len(raw), name)).encode())
        except Exception as e:  # noqa
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
print("GeoGebra generator: http://localhost:%d/generator.html" % PORT)
print("Saving .ggb files to: %s" % OUT)
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
