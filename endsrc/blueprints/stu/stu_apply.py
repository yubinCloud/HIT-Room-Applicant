from flask import Blueprint, request, jsonify

from endsrc.models import Apply
from endsrc.extensions import db
import datetime



stu_apply = Blueprint('stu_apply', __name__)
@stu_apply.route('', methods = ['GET','POST'])
def Stu_Apply():
    global result_data
    if request.method == 'POST':
        json_data = request.get_json(silent=True)

        if json_data is None:
            return jsonify(code=-101, data=None)

        if not json_data.get('activity_name') :
            return jsonify(code=-101, data={'tip': json_data.get('activity_name')})
        if not json_data.get('begin_time') :
            return jsonify(code=-101, data={'tip': '缺少教室开始使用时间参数'})
        if not json_data.get('activity_date') :
            return jsonify(code=-101, data={'tip': '缺少活动使用日期参数'})
        if not json_data.get('end_time') :
            return jsonify(code=-101, data={'tip': '缺少教室结束使用时间参数'})
        #if not json_data.get('org') :
        #    return jsonify(code=-101, data={'tip': '缺少负责审核的组织参数'})
        if not json_data.get('applicant_id') :
            return jsonify(code=-101, data={'tip': '缺少申请人学号参数'})
        if not json_data.get('applicant_name') :
            return jsonify(code=-101, data={'tip': '缺少申请人姓名参数'})
        if not json_data.get('applicant_phone') :
            return jsonify(code=-101, data={'tip': '缺少申请人联系方式参数'})
        if not json_data.get('people_num') :
            return jsonify(code=-101, data={'tip': '缺少参加人数参数'})
        if not json_data.get('leader_name') :
            return jsonify(code=-101, data={'tip': '缺少负责教师姓名参数'})


        room = Apply()
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        apply_id = str(len(Apply.query.all())+1)
        room.apply_id = apply_id
        room.activity_name = json_data.get('activity_name')
        room.applicant_id = json_data.get('applicant_id')
        room.applicant_name = json_data.get('applicant_name')
        room.applicant_phone = json_data.get('applicant_phone')
        room.apply_time = time
        room.use_date = json_data.get('activity_date')
        room.begin_time = json_data.get('begin_time')
        room.end_time = json_data.get('end_time')
        room.people_count = json_data.get('people_num')
        room.requests = json_data.get('requests')
        #room.org = json_data.get('org')
        room.teacher_name = json_data.get('leader_name')
        #room.material = json_data.get('material')
        room.check_status = '待审核'

        Apply(room)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'tip': '数据库异常'})

        return jsonify(code=0,data={'tip': '正常'})

    elif request.method == 'GET':
        # 获取学生学号
        stu_id = '181320429'
        records = Apply.query.filter(Apply.applicant_id == stu_id).all()
        result_data = list()

        status_map = {
            '待审核' : 0,
            '审核通过' : 1,
            '审核失败' : 2,
        }

        for record in records:
            result_data.append(dict(
                apply_id=record.apply_id,
                building=record.building,
                floor=record.floor,
                room=record.room_name,
                date=record.use_date,
                begin_time=record.begin_time,
                end_time=record.end_time,
                check_status=status_map.get(record.check_status)
            ))

    return jsonify(code=0,data=result_data)
