import json
import http.server
import database as db
from mimetypes import MimeTypes


class Handler(http.server.BaseHTTPRequestHandler):

    def _file(self):
        filename = self.path
        mime = MimeTypes()
        mimetype, encoding = mime.guess_type(filename)
        try:
            fd = open(f'./files/{filename}', 'rb')
            content = fd.read()
            fd.close()
            self.send_response(200)
            self.send_header('Content-Type', mimetype)
            self.end_headers()
            self.wfile.write(content)
        except BaseException:
            self.send_response(404, 'File not found')
            self.end_headers()

    def _database(self, args: list):
        if len(args) != 2:
            self.send_response(400, 'Incorrect endpoint: missing table name')
            self.end_headers()
            return

        table = args[1]
        size = int(self.headers.get('Content-Length'))
        data = self.rfile.read(size)
        try:
            input = json.loads(data)
        except json.decoder.JSONDecodeError as e:
            self.send_response(500, e.args[0])
            self.end_headers()
            return

        output = json.dumps(db.execute(table, input))

        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

        self.send_response(200, 'Ok')
        for name in headers.keys():
            self.send_header(name, headers[name])
        self.end_headers()

        self.wfile.write(bytes(output, 'utf-8'))
        return

    def do_GET(self):
        self._file()

    def do_POST(self):
        endpoints = self.path.split('/')[1:]
        if len(endpoints) < 1:
            self.send_response(400, 'Resource not specified')
            self.end_headers()

        router = {
            'database': self._database
        }

        if endpoints[0] not in router:
            self.send_response(404, 'Resource not found')
            self.end_headers()

        router[endpoints[0]](endpoints)
        return

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
