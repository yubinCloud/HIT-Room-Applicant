# http://xx.com/api/stu/timetable

from flask import Blueprint, jsonify
from endsrc.models import Timetable

time_get = Blueprint('time_get', __name__)


@time_get.route('/', methods=['GET'])
def get_timetable():
    Time = Timetable.query.all()  # 获取所有时间信息
    data_time = []
    for i in Time:
        data_time.append(['第'+str(i.class_id)+'节', i.begin_time, i.end_time ])
    return jsonify(code=0, data=data_time)