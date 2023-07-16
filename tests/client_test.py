from client import Client


def insert_person(name: str, surname: str) -> dict:
    return {
        "action": "insert",
        "data": {
            'name': name,
            'surname': surname
        }
    }


def update_person(id: int, data: dict) -> dict:
    return {
        "action": "update",
        "data": data,
        "cond": {
            "rowid": {"_eq": id}
        }
    }


def delete_person(id: int) -> dict:
    return {
        "action": "delete",
        "cond": {
            "rowid": {"_eq": id}
        }
    }


def list_people(cond: dict) -> dict:
    return {
        "action": "select",
        "data": {
            "rowid": True, "name": True, "surname": True
        },
        "cond": cond
    }


if __name__ == '__main__':

    C = Client('localhost', 9000)

    resp = C.query('people', insert_person('Heli', 'Barrocas'))
    if resp['status'] != 'Ok':
        print(f"Database error: {resp['status']}")

    if resp['affectedRows'] == 1:
        print(f"Successfully added row. New row ID = {resp['insertId']}")

    filter = {}
    list = C.query('people', list_people(filter))

    if list['status'] == 'Ok':
        data = list['data']
        for row in data:
            print(f"{row['rowid']}: {row['name']}, {row['surname']}")
