from flask import Blueprint, jsonify, request, session
from models import Room, Administrator
from extensions import db

adm_myroom = Blueprint('adm_myroom', __name__)


@adm_myroom.route('/myroom', methods=['POST'])
#@adm_login_required(post_grades=(1, ))
def Adm_myroom():
    """
    POST：移入/移出教室
    :return:
    """
    # 查找出当前管理员
    cur_account = session.get('admin_login')     # 获取当前用户名
    cur_admin = Administrator.query.filter_by(account=cur_account).first()
    if cur_admin is None:
        return jsonify(code=-102, tip='未查询到该管理员')
    # 获取参数
    rev_json = request.get_json(silent=True)
    shift_type, room_ids = rev_json.get('type'), rev_json.get('id')
    # 验证参数
    if None in (shift_type, room_ids):
        return jsonify(code=-101, tip='缺少必要参数')
    # 根据type进行不同的操作
    if shift_type == 0:
        return shift_out(cur_admin.org, room_ids)    # 移出操作
    elif shift_type == 1:
        return shift_in(cur_admin.org, room_ids)     # 移入操作


@adm_myroom.route('/building', methods=['GET'])
def room_number_fun():
    """
    获取全部楼号
    http://xx.com/api/admin/building
    :return: json
    """
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

def shift_out(org, room_ids):
    """
    对ids所对应的教室全部移出org的管理范围
    :param org: 所要操作的组织
    :param room_ids: 所有的教室id
    :return: 需要返回给前端的数据
    """
    for room_id in room_ids:
        room = Room.query.get(room_id)
        if room is None or room.org != org:
            continue
        room.org = None
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(code=101, tip='数据库异常')
    return jsonify(code=0, data={'tip': '操作成功'})


def shift_in(org, room_ids):
    """
    对ids所对应的教室全部移入org的管理范围
    :param org: 所要操作的组织
    :param room_ids: 所有的教室id
    :return: 需要返回给前端的数据
    """
    for room_id in room_ids:
        room = Room.query.get(room_id)
        if room is None:
            continue
        room.org = org
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(code=101, tip='数据库异常')
    return jsonify(code=0, data={'tip': '操作成功'})