from flask import Blueprint, jsonify
from models import Room

room_info = Blueprint('room_info', __name__)

@room_info.route('', methods = ['GET'])
def RoomInfo(room_id):
    # 在数据库中查找教室信息
    record = Room.query.get(room_id)
    if record is None:
        return jsonify(code = -102, data = {})
    else:
        return jsonify(code = 0, data = {
                "id": record.room_id,
                "org": record.org,
                "picture": record.picture,
                "max_num": record.max_num,
                "description": record.description
            })