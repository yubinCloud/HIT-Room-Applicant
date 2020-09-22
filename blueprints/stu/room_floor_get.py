# http://xx.com/api/stu/building

from flask import Blueprint, jsonify
from models import Room

room_floor_get = Blueprint('room_number_get', __name__)


@room_floor_get.route('/', methods=['GET'])
def room_number_fun():
    room_list = Room.query.all()  # 获取Room表所有教室信息
    s = set()
    for i in room_list:
        s.add(i.building)
    room_data = {}
    for i in s:
        room_data[i] = {}
    for i in room_list:
        if i.floor not in room_data[i.building]:
            room_data[i.building][i.floor] = []
    for i in room_list:
        room_data[i.building][i.floor].append(i.room_name)
    return jsonify(code=0, data=room_data)