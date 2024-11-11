import json


def message(message_: str, code: int):
    return json.dumps({"message": message_}), code, {'Content-Type': 'application/json'}


def json_data(data: dict, code: int):
    return json.dumps(data), code, {'Content-Type': 'application/json'}
