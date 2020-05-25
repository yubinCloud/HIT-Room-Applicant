from flask import Blueprint, jsonify, request
from hitapply.common.functions import adm_login_required
from hitapply.models import Room
from hitapply.extensions import db
from sqlalchemy import and_

adm_room = Blueprint('adm_room', __name__)


@adm_room.route('', methods=['GET', 'POST'])
# @adm_login_required(get_grades=(1, 2, 3), post_grades=(1,))
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


@adm_room.route('/num', methods=['GET'])
# @adm_login_required(get_grades=(1, 2, 3))
def Adm_room_num():
    """
    GET：获取教室数量
    :return:
    """
    if request.method == "GET":
        return Adm_room_num_GET()


@adm_room.route('/noadmin', methods=['GET'])
# @adm_login_required(get_grades=(1, 2, 3))
def Adm_room_noadmin():
    """
    GET：获取无管理员的教室
    :return:
    """
    # 获取json
    rev_json = request.get_json(silent=True)
    if rev_json is None:
        return jsonify(code=-101, data={'tip': '缺少必要参数'})

    start_id, end_id = rev_json.get('start_id'), rev_json.get('end_id')
    # 验证参数有效性
    room_nums = Room.query.count()
    if start_id > room_nums:
        return jsonify(code=-102, tip='超过教室最大数量')
    rooms = Room.query.filter(and_(Room.room_id >= start_id, Room.room_id <= end_id, Room.org == None)).all()
    res_data = rooms_to_data(rooms)
    return jsonify(code=0, data=res_data)


@adm_room.route('/noadmin/num', methods=['GET'])
# @adm_login_required(get_grades=(1, 2, 3))
def Adm_room_noadmin_num():
    """
    GET：获取无管理员的教室数量
    :return:
    """
    noadmin_room_num = Room.query.filter_by(org=None).count()
    return jsonify(code=0, data=noadmin_room_num)


def Adm_room_GET(rev_json):
    """
    处理Adm_room视图函数的GET请求
    :param rev_json: 接收到的json数据
    :return: 需要发送给前端的结果
    """
    start_id, end_id = rev_json.get('start_id'), rev_json.get('end_id')
    # 验证参数的有效性
    if None in (start_id, end_id):
        return jsonify(code=-101, tip='缺少必要参数')
    room_nums = Room.query.count()
    if start_id > room_nums:
        return jsonify(code=-102, tip='超过教室最大数量')
    if end_id > room_nums:
        end_id = room_nums
    # 查询出所有符合条件的教室
    rooms = Room.query.offset(start_id - 1).limit(end_id - start_id + 1).all()
    res_data = rooms_to_data(rooms)
    return jsonify(code=0, data=res_data)


def rooms_to_data(rooms):
    """
    将rooms转化成一个包含所有room对应字典的列表对象，其中每个字典包含该room的所有信息
    :param rooms:所有待转化的教室
    :return:转化后的data
    """
    return [dict(id=room.room_id,
                 building=room.building,
                 floor=room.floor,
                 room_name=room.room_name,
                 org=room.org,
                 max_num=room.max_num,
                 permissible=room.permissible) for room in rooms]


def Adm_room_POST(rev_json):
    """
    处理Adm_room的POST请求
    :param rev_json: 接收到的json数据
    :return: 需要发送给前端的数据
    """
    # 获取参数
    building = rev_json.get('building')
    floor = rev_json.get('floor')
    org = rev_json.get('org')
    room_name = rev_json.get('room_name')
    picture = rev_json.get('picture')
    max_num = rev_json.get('max_num')
    description = rev_json.get('description')
    permissible = True if rev_json.get('permission') != 0 else False
    # 验证必需参数
    if None in (building, floor, room_name, max_num, permissible):
        return jsonify(code=-101, data={'tip': '缺少必要参数'})

    newRoom = Room(building=building,
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


def Adm_room_num_GET():
    """
    处理Adm_room_num的GET请求
    :return: 需要返回给前端的数据
    """
    return jsonify(code=0, data={'num': Room.query.count()})
