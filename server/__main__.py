import getopt
import os
import sys
from http.server import ThreadingHTTPServer
from httpserver import Handler

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
