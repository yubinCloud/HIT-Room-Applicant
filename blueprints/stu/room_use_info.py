from flask import Blueprint, request, jsonify
from models import Room, Apply, Timetable

room_use_info = Blueprint('room_use_info', __name__)

@room_use_info.route('', methods = ['GET'])
def RoomUseInfo(room_id):
    date = request.args.get("date")
    time = request.args.get("time")
    if not (date and time):
        # 缺请求参数
        return jsonify(code = -101, data = {})
    
    # 根据房间号获取房间名
    data = Room.query.filter(Room.room_id == room_id).first()
    if not data:
        return jsonify(code = -102, data = {})
    room_name = data.room_name

    # 获取所属组织和活动名
    duration = Timetable.query.filter(Timetable.class_id == time).first()
    if not duration:
        return jsonify(code = -102, data = {})
    begin_time = duration.begin_time
    end_time = duration.end_time

    result = Apply.query.filter(Apply.begin_time == begin_time, Apply.end_time == end_time, 
                                Apply.use_date == date, Apply.room_name == room_name).first()
    if not result:
        return jsonify(code = -102, data = {})
    else:
        return jsonify(code = 0, data = {"organization": result.applicant_name, "activity": result.activity_name})
        