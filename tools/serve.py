# Local preview that behaves like Netlify: /about serves about.html, unknown URLs get 404.html.
#   python3 build.py && python3 tools/serve.py   → http://localhost:8000
import http.server, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'abhishek-really-site')
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def send_head(self):
        path = self.path.split('?')[0].split('#')[0]
        if path != '/' and '.' not in os.path.basename(path) and os.path.exists(os.path.join(ROOT, path.lstrip('/') + '.html')):
            self.path = path + '.html'
        elif not os.path.exists(os.path.join(ROOT, path.lstrip('/'))):
            self.path = '/404.html'
        return super().send_head()
http.server.ThreadingHTTPServer(('', int(sys.argv[1]) if len(sys.argv) > 1 else 8000), H).serve_forever()
