from flask import Blueprint, jsonify, request
from models import Room, Apply, Timetable
from sqlalchemy import and_
from common import utils

room = Blueprint('room', __name__)


# 以下函数均用于帮助获取教室使用情况
# 创建一个原始的res_data
def create_res_data(rooms, timetable_len):
    res_data = dict()
    for room in rooms:
        floor = str(room.floor)
        if floor not in res_data:
            res_data[floor] = dict()

        res_data[floor][room.room_name] = dict(id=room.room_id, use=[True] * timetable_len)

    return res_data


# 将一个时间点对应到第几大节
def time_to_class(time, timetable, is_begin=True):
    if is_begin:
        for period in timetable:
            if period.begin_time <= time < period.end_time:
                return period.class_id
    else:
        for period in timetable:
            if period.begin_time < time <= period.end_time:
                return period.class_id
    return None


# 返回时间表中最小的节数
def min_class_id(timetable):
    min_class = 50
    for period in timetable:
        if period.class_id < min_class:
            min_class = period.class_id
    return min_class


# 返回时间表中最大的节数
def max_class_id(timetable):
    max_class = -1
    for period in timetable:
        if period.class_id > max_class:
            max_class = period.class_id
    return max_class


# 根据申请记录修改教室状态
def modify_room_status(room_status, record, timetable):
    begin_class = time_to_class(record.begin_time, timetable, is_begin=True)
    end_class = time_to_class(record.end_time, timetable, is_begin=False)

    # 异常情况
    if begin_class is None and end_class is None:
        return
    if begin_class is None:
        begin_class = min_class_id(timetable)
    if end_class is None:
        end_class = max_class_id(timetable)

    for i in range(begin_class - 1, end_class):
        room_status[i] = False


# 根据申请记录修改 res_data
def modify_res_data(res_data, records, timetable):
    for record in records:
        cur_floor = res_data.get(str(record.floor))
        if cur_floor is None:
            continue
        room_status = cur_floor.get(record.room_name)
        if room_status is None:  # 说明所申请到的教室不在教室信息表中
            continue
        else:
            modify_room_status(room_status['use'], record, timetable)


# GET:查看教室使用情况
@room.route('/room/use')
def stu_room_use_info():
    # 获取json
    date = request.args.get('date')
    building = request.args.get('building')
    # 检查json数据是否有缺少
    if date is None or building is None:
        return jsonify(code=-101, data=None)
    # 获取时间表的信息
    timetable = Timetable.query.all()

    # 获取符合条件的全部教室 rooms 并生成初始化的结果数据 res_data
    rooms = Room.query.filter(and_(Room.building == building))
    res_data = create_res_data(rooms, len(timetable))

    # 查询申请信息表中符合查询条件的申请记录
    records = Apply.query.filter(and_(Apply.check_status == "审核通过", Apply.use_date == date,
                                      Apply.building == building)).all()

    # 根据申请记录修改 res_data
    modify_res_data(res_data, records, timetable)

    return jsonify(code=0, data=res_data)

# 获取全部楼号
@room.route('/building', methods=['GET'])
def room_number_fun():
    """
    获取全部楼号
    http://xx.com/api/stu/building
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

# 查看教室使用说明
@room.route('/room/use/<string:room_id>', methods=['GET'])
def RoomUseInfo(room_id):
    """
    查看教室使用说明
    :param room_id:在Room数据表中的主键
    :return:json
    """
    date = request.args.get("date")
    time = request.args.get("time")
    if not (date and time):
        # 缺请求参数
        return jsonify(code=-101, data={})

    # 根据房间号获取房间名
    data = Room.query.filter(Room.room_id == room_id).first()
    if not data:
        return jsonify(code=-102, data={})
    room_name = data.room_name

    # 获取所属组织和活动名
    duration = Timetable.query.filter(Timetable.class_id == time).first()
    if not duration:
        return jsonify(code=-102, data={})
    begin_time = duration.begin_time
    end_time = duration.end_time
    result = Apply.query.filter(Apply.begin_time == begin_time and Apply.end_time == end_time and
                                Apply.use_date == date and Apply.room_name == room_name).first()
    if not result:
        return jsonify(code=-102, data={})
    else:
        return jsonify(code=0, data={"organization": result.applicant_name, "activity": result.activity_name})


# 查看教室介绍
@room.route('/room/<string:room_id>', methods=['GET'])
def RoomInfo(room_id):
    # 在数据库中查找教室信息
    record = Room.query.get(room_id)
    if record is None:
        return jsonify(code=-102, data={})
    else:
        return jsonify(code=0, data={
            "id": record.room_id,
            "org": record.org,
            "picture": record.picture,
            "max_num": record.max_num,
            "description": record.description
        })
