import http.server
import socketserver
import os

PORT = 8000

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the file directly if it exists (e.g. css, js, images)
        if os.path.exists(self.translate_path(self.path)):
            super().do_GET()
            return

        # If not, try appending .html
        path_with_html = self.path + ".html"
        if os.path.exists(self.translate_path(path_with_html)):
            self.path = path_with_html
            super().do_GET()
            return

        # Fallback to 404 (or default behavior)
        super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("clean URLs are supported (e.g. /contact will serve /contact.html)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
