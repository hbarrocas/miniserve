import miniserve.builtin as builtin
import getopt
import os
import sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class Handler(BaseHTTPRequestHandler):
    def _parse_url(self):
        self.url = urlparse(self.path)
        self.endpoints = self.url.path.split('/')[1:]
        if len(self.endpoints) < 1:
            self.send_response(400, 'Function not specified')
            self.end_headers()

    def do_GET(self):
        self._parse_url()

        try:
            function = getattr(builtin.GET, self.endpoints[0], False)
            if function is False:
                import functions
                function = getattr(functions.GET, self.endpoints[0])
            function(self)
        except BaseException as e:
            print(f'GET: Error executing function {self.endpoints[0]}:')
            print(e.args[0])
            self.send_response(
                500, 'Error executing function {self.endpoints[0]}'
            )
            self.end_headers()

    def do_POST(self):
        self._parse_url()

        try:
            function = getattr(builtin.POST, self.endpoints[0])
            function(self)
        except BaseException:
            print(f'POST: Error executing function {self.endpoints[0]}')
            self.send_response(
                500, 'Error executing function {self.endpoints[0]}'
            )
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200, 'Ok')
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        for name in headers.keys():
            self.send_header(name, headers[name])
        self.end_headers()
        return


if __name__ == "__main__":
    OPT_HOST = '-h'
    OPT_PORT = '-p'
    OPT_ROOT = '-r'

    settings = {
        OPT_HOST: '0.0.0.0',
        OPT_PORT: '9000',
        OPT_ROOT: './',
    }

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h:p:r:')
        for opt in opts:
            settings[opt[0]] = opt[1]
    except getopt.GetoptError as e:
        print(e.args[0])
        sys.exit(1)

    host = settings[OPT_HOST]
    port = int(settings[OPT_PORT])
    root = settings[OPT_ROOT]

    os.chdir(root)
    sys.path.append(os.getcwd())

    with ThreadingHTTPServer((host, port), Handler) as httpd:
        print(f'HTTP Server - Listening on port {port}')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            pass

        httpd.server_close()
        print('HTTP Server - Closed')
