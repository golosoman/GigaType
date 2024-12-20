from typing import List
from flask import Blueprint, request, make_response
from sqlalchemy import select

from app import db
from app.models import KeyBoardZone
from app.utils import login_required, send_json_data, make_json_response, message

# Создаем Blueprint для клавиатурных зон
keyboard_zone_api = Blueprint('keyboard_zone_api', __name__, url_prefix="/zone")

@keyboard_zone_api.route("/get", methods=["GET"])
@login_required
def get_keyboard_zones():
    uid = request.args.get('uid', None)  # Получаем uid из параметров запроса

    if uid:
        # Если uid указан, ищем конкретную зону клавиатуры по uid
        zone = db.session.execute(select(KeyBoardZone).where(KeyBoardZone.uid == uid)).first()
        if not zone:
            return message("Неверный uid.", 404)
        zone: KeyBoardZone = zone[0]
        return send_json_data(make_json_response(zone, additional=['uid'], exclude=["keys"]))
    else:
        # Если uid не указан, получаем все зоны клавиатуры
        zones = [zone[0] for zone in db.session.execute(select(KeyBoardZone)).all()]
        # zones.sort(key=lambda x: int(x.__getattribute__("keys")))
        return send_json_data(make_json_response(zones, additional=["uid"]))
