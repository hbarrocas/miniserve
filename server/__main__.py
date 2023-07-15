from http.server import ThreadingHTTPServer
from httpserver import Handler

PORT = 9000

with ThreadingHTTPServer(('', PORT), Handler) as httpd:
    print(f'HTTP Server - Listening on port {PORT}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        pass

    httpd.server_close()
    print('HTTP Server - Closed')
