import http.client
import json


class Client:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def query(self, table: str, structure: dict) -> dict:
        data_out = json.dumps(structure)
        conn = http.client.HTTPConnection(self.host, self.port)
        headers = {'Content-Type': 'application/json'}
        conn.request('POST', f'/database/{table}', data_out, headers)

        resp = conn.getresponse()
        data_in = resp.read()
        conn.close()
        return json.loads(data_in)
