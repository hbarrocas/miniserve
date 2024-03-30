import json
import miniserve.builtin.database as db


def database(server):
    args = server.url.path.split('/')[1:]
    if len(args) < 2:
        server.send_response(400, 'database: missing table name')
        server.end_headers()
        return

    table = args[1]
    size = int(server.headers.get('Content-Length'))
    data = server.rfile.read(size)
    try:
        input = json.loads(data)
    except json.decoder.JSONDecodeError as error:
        server.send_response(500, error.args[0])
        server.end_headers()
        return

    output = json.dumps(db.execute(table, input))

    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }

    server.send_response(200, 'Ok')
    for name in headers.keys():
        server.send_header(name, headers[name])
    server.end_headers()

    server.wfile.write(bytes(output, 'utf-8'))
    return
