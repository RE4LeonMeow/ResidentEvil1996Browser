"""Local preview only. Run: python3 serve.py, then open http://localhost:8000"""
import http.server,pathlib
from functools import partial
root=pathlib.Path(__file__).resolve().parent
class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control','no-cache')
        super().end_headers()
print('Open http://localhost:8000 — select your game files in the browser. Ctrl+C stops the preview.')
http.server.ThreadingHTTPServer(('127.0.0.1',8000),partial(Handler,directory=str(root))).serve_forever()
