from flask import Blueprint, jsonify, request, session

from common.utils import adm_login_required, send_json, record_exception
from models import Room, Administrator
from extensions import db
from sqlalchemy import and_

adm_room = Blueprint('adm_room', __name__)


@adm_room.route('', methods=['GET', 'POST'])
@adm_login_required(get_grades=(1, 2, 3), post_grades=(1, 3))
def Adm_room():
    """
    GET：查看教室列表
    POST：新增教室
    :return:
    """
    if request.method == 'GET':
        rev_json = request.args
        admin_name = session.get('admin_login')
        admin = Administrator.query.filter(Administrator.account == admin_name).first()
        org = admin.org
        return Adm_room_GET(rev_json, org)
    if request.method == 'POST':
        # 获取json
        rev_json = request.get_json(silent=True)
        if rev_json is None:
            return jsonify(code=-101, data={'tip': '缺少必要参数'})
        return Adm_room_POST(rev_json)


@adm_room.route('/num', methods=['GET'])
@adm_login_required(get_grades=(1, 2, 3))
def Adm_room_num():
    """
    GET：获取教室数量
    :return:
    """
    if request.method == "GET":
        cur_account = session.get('admin_login')  # 获取当前用户名

        return Adm_room_num_GET(cur_account)


@adm_room.route('/noadmin', methods=['GET'])
# @adm_login_required(get_grades=(1, 2, 3))
def Adm_room_noadmin():
    """
    GET：获取无管理员的教室
    :return:
    """
    # 获取json
    rev_json = request.args
    if rev_json is None:
        return jsonify(code=-101, data={'tip': '缺少必要参数'})

    start_id, end_id = rev_json.get('start_id'), rev_json.get('end_id')
    # 验证参数有效性
    room_nums = Room.query.count()
    if start_id > room_nums:
        return jsonify(code=-102, data={'tip': '超过教室最大数量'})
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
    dic = {}
    dic['num'] = noadmin_room_num
    return jsonify(code=0, data=dic)


@adm_room.route('/<string:room_id>', methods=['GET', 'POST'])
# @adm_login_required(get_grades=(1, 2, 3))
def Adm_room_info(room_id):
    """
    GET：查看教室信息
    POST：修改教室信息
    :param room_id:
    :return:
    """
    if request.method == 'GET':
        room = Room.query.get(room_id)
        result_data = {
            'building': room.building,
            'floor': room.floor,
            'room_name': room.room_name,
            'org': room.org,
            'permissible': room.permissible,
            'picture': room.picture,
            'description': room.description
        }
        return send_json(0, result_data)
    else:
        rev_json = request.get_json(silent=True)

        opr_type = rev_json.get('type')
        if opr_type is None: return send_json(-101, '缺少type参数')

        room = Room.query.get(room_id)
        room_name = room.room_name

        if opr_type == 'delete':
            db.session.delete(room)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                record_exception(e)
                return send_json(-101, '数据库异常')
            # return send_json(0, '教室 {} 信息删除成功'.format(room_name))
            return send_json(0, '操作成功')
        elif opr_type == 'update':
            optional_args = {'building', 'floor', 'room_name', 'picture', 'max_num', 'description', 'permissible'}
            for k, v in rev_json.items():
                if k in optional_args:
                    room.__setattr__(k, v)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                record_exception(e)
                return send_json(-101, '数据库异常')
            # return send_json(0, '教室 {} 信息更新成功'.format(room_name))
            return send_json(0, '操作成功')
        else:
            return send_json(-102, '对数据库的操作类型错误')






def Adm_room_GET(rev_json, org):
    """
    处理Adm_room视图函数的GET请求
    :param rev_json: 接收到的json数据。
    :return: 需要发送给前端的结果
    """
    start_id, end_id = rev_json.get('start_id'), rev_json.get('end_id')
    # 验证参数的有效性
    if None in (start_id, end_id):
        return jsonify(code=-101, tip='缺少必要参数')
    try:
        start_id = int(start_id)
        end_id = int(end_id)
    except Exception:
        return send_json(-102, 'start_id 或 end_id 值错误')
    room_nums = Room.query.count()
    if start_id > room_nums:
        return jsonify(code=-102, tip='超过教室最大数量')
    if end_id > room_nums:
        end_id = room_nums
    # 查询出所有符合条件的教室
    rooms = Room.query.offset(start_id - 1).limit(end_id - start_id + 1).all()
    res_data = rooms_to_data(rooms, org)
    return jsonify(code=0, data=res_data)


def rooms_to_data(rooms, org):
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
                 permissible=room.permissible) for room in rooms if room.org == org]


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
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return jsonify(data={'tip': '教室添加成功'})


def Adm_room_num_GET(cur_account):
    """
    处理Adm_room_num的GET请求
    :return: 需要返回给前端的数据
    """
    cur_admin = Administrator.query.filter_by(account=cur_account).first()
    cur_org = cur_admin.org
    return jsonify(code=0, data={'num': len(Room.query.filter(Room.org == cur_org).all())})
