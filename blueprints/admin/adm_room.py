from flask import Blueprint, jsonify, request
from hitapply.common.functions import adm_login_required
from hitapply.models import Room
from hitapply.extensions import db

adm_room = Blueprint('adm_room', __name__)


@adm_room.route('', methods=['GET', 'POST'])
@adm_login_required(get_grades=(1, 2, 3), post_grades=(1,))
def Adm_room():
    """
    GET：查看教室列表
    POST：新增教室
    :return:
    """
    # 获取json
    rev_json = request.get_json(silent=True)
    if rev_json is None:
        return jsonify(code=-101, data={'tip': '缺少必要参数'})

    if request.method == 'GET':
        return Adm_room_GET(rev_json)
    if request.method == 'POST':
        return Adm_room_POST(rev_json)


def Adm_room_GET(rev_json):
    pass


def Adm_room_POST(rev_json):
    # 获取参数
    building = rev_json.get('building')
    floor = rev_json.get('floor')
    org = rev_json.get('org', 'school')
    room_name = rev_json.get('room_name')
    picture = rev_json.get('picture')
    max_num = rev_json.get('max_num')
    description = rev_json.get('description')
    permissible = True if rev_json.get('permission') != 0 else False
    # 验证必需参数
    if None in (building, floor, room_name, max_num, permissible):
        return jsonify(code=-101, data={'tip': '缺少必要参数'})

    newRoom = Room(room_id=str(Room.query.count() + 1),
                   building=building,
                   floor=floor,
                   org=org,
                   room_name=room_name,
                   picture=picture,
                   max_num=max_num,
                   description=description,
                   permissible=permissible)
    db.session.add(newRoom)
    db.session.commit()
    return jsonify(data={'tip': '教室添加成功'})
