# http://xx.com/stu/room/use

from flask import Blueprint, request, jsonify
from sqlalchemy import and_

from hitapply.models import Apply, Room, Timetable
from hitapply.common import functions

stu_room_use = Blueprint('stu_room_use', __name__)


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
            max_class = period
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
@stu_room_use.route('/')
def stu_room_use_info():
    # 获取json
    rev_json = request.get_json(silent=True)

    # 检查json数据是否有缺少
    try:
        functions.check_key(rev_json, 'data', 'building')
    except KeyError:
        return jsonify(code=-101, data=None)

    # 解析json数据
    date = rev_json.get('date')
    building = rev_json.get('building')

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
