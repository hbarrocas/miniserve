from client import Client


def insert_image(name: str, pixeldata: str) -> dict:
    return {
        "action": "insert",
        "data": {
            'name': name,
            'pixeldata': pixeldata
        }
    }


def update_image(id: int, data: dict) -> dict:
    return {
        "action": "update",
        "data": data,
        "cond": {
            "rowid": {"_eq": id}
        }
    }


def read_image(id: int) -> dict:
    return {
        "action": "select",
        "data": {"rowid": True, "pixeldata": True},
        "cond": {
            "rowid": {"_eq": id}
        }
    }


def delete_image(id: int) -> dict:
    return {
        "action": "delete",
        "cond": {
            "rowid": {"_eq": id}
        }
    }


def list_images(cond: dict) -> dict:
    return {
        "action": "select",
        "data": {
            "rowid": True, "name": True
        },
        "cond": cond
    }


if __name__ == '__main__':
    import json

    C = Client('localhost', 9000)

    '''
    data = []
    img = open('image.txt')
    for row in img.readlines():
        data.append([0 if ch == '.' else 1 for ch in list(row)])

    r = C.query('image', update_image(1, {'pixeldata': json.dumps(data)}))
    print(r['status'])
    '''

    resp = C.query('image', read_image(1))
    if resp['status'] != 'Ok':
        print(f"Error: {resp['status']}")
    else:
        data = resp['data'][0]

        for row in json.loads(data['pixeldata']):
            print(" ".join(['.' if px == 0 else 'x' for px in row]))
