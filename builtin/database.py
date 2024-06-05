import sqlite3
import miniserve.builtin.query as q


def row_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def execute(database: str, table: str, data: dict) -> dict:

    response = {
        'status': 'Ok',
        'data': [],
        'affectedRows': -1,
        'insertId': 0
    }

    try:
        if 'action' not in data:
            raise Exception(
                'An action has to be specified (insert|update|select|delete)'
            )

        action = data['action']
        cond = data['cond'] if 'cond' in data else {}
        order = data['order'] if 'order' in data else {}
        limit = data['limit'] if 'limit' in data else False
        offset = data['offset'] if 'offset' in data else 0
        page = (limit, offset) if limit is not False else False

        if 'data' not in data and action != 'delete':
            raise Exception('data field is required for this operation')

        fields = data['data'] if 'data' in data else {}

        if action == 'insert':
            query, values = q.insert(table, fields)
        elif action == 'update':
            query, values = q.update(table, fields, cond)
        elif action == 'select':
            query, values = q.select(table, fields, cond, order, page)
        elif action == 'delete':
            query, values = q.delete(table, cond)
        else:
            raise Exception(f'Unknown action {action}')

        conn = sqlite3.connect(f'{database}.db')
        conn.row_factory = row_factory
        c = conn.cursor()

        resp = c.execute(query, values)
        response['data'] = resp.fetchall()
        response['affectedRows'] = c.rowcount
        response['insertId'] = c.lastrowid

        conn.commit()
        conn.close()
    except BaseException as e:
        response['status'] = e.args[0]

    return response


if __name__ == "__main__":
    import sys
    import json

    jsoninput = "".join(list(sys.stdin))
    data = json.loads(jsoninput)
    response = execute('people', data)
    jsonoutput = json.dumps(response)

    print(jsonoutput)
