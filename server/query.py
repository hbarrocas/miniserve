
def _validate_table(table: str):
    if len(table) == 0:
        raise Exception('Table name cannot be an empty string')


def _fields_name(data: dict) -> str:
    return ", ".join(list(data.keys()))


def _fields_assign(data: dict) -> str:
    return ", ".join(["{0} = ?".format(field) for field in data.keys()])


def _fields_value(data: dict) -> list:
    return list(data.values())


def _cond_op(value: dict) -> str:
    map_op = {
        '_eq': '=',
        '_like': 'like',
        '_gt': '>',
        '_gteq': '>=',
        '_lt': '<',
        '_lteq': '<='
    }
    if len(value) != 1:
        raise Exception('Expected 1 operator and value')
    op = list(value.keys())[0]
    if op not in map_op:
        raise Exception(f'Unknown operator "{op}"')
    return f'{map_op[op]} ?'


def _conds_value(cond: dict) -> list:
    return [list(op.values())[0] for op in cond.values()]


def _where(cond: dict) -> str:
    if len(cond) == 0:
        return ''
    conds = " AND ".join([f'{c} {_cond_op(v)}' for c, v in cond.items()])
    return f'WHERE {conds}'


def _order_dir(dir: str) -> str:
    map_ord = {
        '_asc': 'ASC',
        '_desc': 'DESC'
    }
    if dir not in map_ord:
        raise Exception('Sorting order can only be _asc or _desc')
    return map_ord[dir]


def _order_by(order: dict) -> str:
    ord = ", ".join([
        f'{field} {_order_dir(dir)}' for field, dir in order.items()
    ])
    return f'ORDER BY {ord}'


def _limit(page: tuple[int, int]) -> str:
    limit, offset = page
    lim = f'{offset}, {limit}' if offset > 0 else f'{limit}'
    return f'LIMIT {lim}'


def select(
    table: str,
    data: dict,
    cond: dict,
    order: dict,
    page: tuple[int, int]
) -> (str, list):
    _validate_table(table)
    fields = _fields_name(data) if len(data) > 0 else '*'
    query_data = []
    query_template = 'SELECT {1} FROM {0}'
    query_blocks = [query_template.format(table, fields)]
    if len(cond) > 0:
        query_blocks.append(_where(cond))
        query_data.extend(_conds_value(cond))
    if len(order) > 0:
        query_blocks.append(_order_by(order))
    if page is not False:
        query_blocks.append(_limit(page))

    query = " ".join(query_blocks)
    return (query, query_data)


def insert(table: str, data: dict) -> (str, list):
    _validate_table(table)
    if len(data) == 0:
        raise Exception('Data dictionary empty; no data to insert?')

    fields = _fields_name(data)
    values = ", ".join(["?" for field in range(len(data))])
    query_data = _fields_value(data)
    query_template = 'INSERT INTO {0} ({1}) VALUES ({2})'
    query = query_template.format(table, fields, values)
    return (query, query_data)


def update(table: str, data: dict, cond: dict) -> (str, list):
    _validate_table(table)
    if len(data) == 0:
        raise Exception('Data dictionary empty; no data to update?')

    fields = _fields_assign(data)
    query_data = _fields_value(data)
    query_template = 'UPDATE {0} SET {1}'
    query_blocks = [query_template.format(table, fields)]
    if len(cond) > 0:
        query_blocks.append(_where(cond))
        query_data.extend(_conds_value(cond))

    query = " ".join(query_blocks)
    return (query, query_data)


def delete(table: str, cond: dict) -> (str, list):
    _validate_table(table)
    query_data = []
    query_template = 'DELETE FROM {0}'
    query_blocks = [query_template.format(table)]
    if len(cond) > 0:
        query_blocks.append(_where(cond))
        query_data.extend(_conds_value(cond))

    query = " ".join(query_blocks)
    return (query, query_data)
