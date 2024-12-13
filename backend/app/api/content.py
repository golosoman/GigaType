from random import choices, choice, randint
from typing import List

from flask import Blueprint, request, make_response
from sqlalchemy import select, and_, delete

from app import db
from app.models import Difficulty, KeyBoardZone
from app.utils import (admin_required, message, send_json_data, check_all_args, check_one_arg, make_json_response,
                       util_round, login_required)

content_api = Blueprint('content_api', __name__, url_prefix="/content")


@content_api.route("/generate", methods=["POST"])
@admin_required
def generate():
    data = request.json
    if 'uids' not in data or "length" not in data:
        return message("Недостаточно данных")

    zones = [zone[0].keys for zone in
             db.session.execute(select(KeyBoardZone).where(KeyBoardZone.uid.in_(data['uids']))).all()]
    available_chars = "".join(zones)
    try:
        int(data['length'])
    except ValueError as e:
        print(str(e))
        return message("Кол-во символов для генерации должно быть числом")
    # Простейшая генерация
    # content = " "
    # while len(content) < int(data['length']):
    #     if len(content.split(" ")[-1]) == 7:
    #         content += " "
    #     chosen_char = choice(available_chars)
    #     if content[-1] == " " and chosen_char == " ":
    #         continue
    #     content += chosen_char
    # content = content[1:]

    # Чуть поинтереснее
    content = ""
    prev_chunk_length = 0
    while len(content) < int(data['length']):
        print(f"{(len(content)/int(data['length']))*100}%")
        if content:
            content += " "
        while True:
            base_chunk_length = randint(2, 7)
            if base_chunk_length != prev_chunk_length:
                prev_chunk_length = base_chunk_length
                break
        base_chunk = "".join(choices(available_chars, k=base_chunk_length))
        content += " ".join([base_chunk for _ in range(randint(1, 5))])
    content = content[:int(data['length'])]
    content = content.strip()
    if len(content) != int(data['length']):
        content += "".join(choices(available_chars, k=int(data['length'])-len(content)))
    return send_json_data({"content": content, "length": len(content)})
