from mimetypes import MimeTypes


def files(server):
    filename = f'./{server.url.path}'
    mime = MimeTypes()
    mimetype, encoding = mime.guess_type(filename)
    try:
        fd = open(filename, 'rb')
        content = fd.read()
        fd.close()
        server.send_response(200)
        server.send_header('Content-Type', mimetype)
        server.end_headers()
        server.wfile.write(content)
    except BaseException:
        server.send_response(404, 'File not found')
        server.end_headers()
