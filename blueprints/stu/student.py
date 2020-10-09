from flask import Blueprint, request, jsonify

from models import Apply, Room
from extensions import db
import datetime

student = Blueprint('student', __name__)


# 从session中获得applicant_id
def from_session_get_applicant_id():
    return '181320521'

# http://xxx/api/stu/apply
# GET：获得所有申请的列表。
# POST：提交教室申请。
@student.route('', methods=['GET', 'POST'])
def Stu_Apply():
    global result_data
    if request.method == 'POST':
        # 学生提交申请
        json_data = request.get_json(silent=True)

        if json_data is None:
            return jsonify(code=-101, data=None)

        if not json_data.get('activity_name'):
            return jsonify(code=-101, data={'tip': '缺少活动名称参数'})

        '''
        if not json_data.get('applicant_id'):
            return jsonify(code=-101, data={'tip': '缺少申请人学号参数'})
        '''

        if not json_data.get('applicant_name'):
            return jsonify(code=-101, data={'tip': '缺少申请人姓名参数'})

        if not json_data.get('applicant_phone'):
            return jsonify(code=-101, data={'tip': '缺少申请人联系方式参数'})

        if not json_data.get('use_date'):
            return jsonify(code=-101, data={'tip': '缺少活动使用日期参数'})

        if not json_data.get('begin_time'):
            return jsonify(code=-101, data={'tip': '缺少教室开始使用时间参数'})

        if not json_data.get('end_time'):
            return jsonify(code=-101, data={'tip': '缺少教室结束使用时间参数'})

        if not json_data.get('people_count'):
            return jsonify(code=-101, data={'tip': '缺少参加人数参数'})

        if not json_data.get('teacher_name'):
            return jsonify(code=-101, data={'tip': '缺少负责教师姓名参数'})

        if not json_data.get('building'):
            return jsonify(code=-101, data={'tip': '缺少教室所在教学楼的参数'})

        if not json_data.get('floor'):
            return jsonify(code=-101, data={'tip': '缺少教室所在楼层参数'})

        if not json_data.get('room'):
            return jsonify(code=-101, data={'tip': '缺少教室名字参数'})

        request_flag = material_flag = 1  # 如果为0，表示post传递的json不含有request_或material字段

        if not json_data.get('request'):
            request_flag = 0
        if not json_data.get('material'):
            material_flag = 0

        building_posted = json_data.get('building')
        floor_posted = json_data.get('floor')
        room_posted = json_data.get('room')
        exist = Room.query.filter(
            Room.room_name == room_posted and Room.floor == floor_posted and Room.building == building_posted).first()
        if exist is None:
            return jsonify(code=-102, data={'tip': '未查询到该教室'})

        room = Apply()
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        apply_id = str(0)
        room.apply_id = apply_id
        room.activity_name = json_data.get('activity_name')
        room.applicant_id = from_session_get_applicant_id()
        room.applicant_name = json_data.get('applicant_name')
        room.applicant_phone = json_data.get('applicant_phone')
        room.apply_time = time
        room.use_date = json_data.get('use_date')
        room.begin_time = json_data.get('begin_time')
        room.end_time = json_data.get('end_time')
        room.people_count = json_data.get('people_count')
        if request_flag:
            room.request = json_data.get('request')
        room.teacher_name = json_data.get('teacher_name')
        if material_flag:
            room.material = json_data.get('material')
        room.check_status = '待审核'
        room.building = json_data.get('building')
        room.floor = json_data.get('floor')
        room.room_name = json_data.get('room')

        db.session.add(room)
        db.session.commit()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'tip': '数据库异常'})

        return jsonify(code=0, data={'tip': '正常'})

    elif request.method == 'GET':
        # 获取所有申请列表
        records = Apply.query.all()
        result_data = list()

        status_map = {
            '待审核': 0,
            '审核通过': 1,
            '审核失败': 2,
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

    return jsonify(code=0, data=result_data)


# ---------------------------------------------------------------------
# http://xxx/api/stu/apply/<string:apply_id>
# GET:获得apply_id对应的申请的详情
# POST:修改apply_id的申请内容

def application_GET(record):
    # 从数据库中取出相应数据
    res_data = {'room_name': record.room_name,
                'building': record.building,
                'floor': record.floor,
                'activity_name': record.activity_name,
                'people_count': record.people_count,
                'applicant_id': record.applicant_id,
                'applicant_name': record.applicant_name,
                'applicant_phone': record.applicant_phone,
                'apply_time': record.apply_time.strftime('%Y-%m-%d %H-%M-%S'),
                'date': record.use_date,
                'begin_time': record.begin_time,
                'end_time': record.end_time,
                'request': record.request,
                'check_status': record.check_status,
                'org': record.org,
                'note': record.note,
                'verifier_name': record.verifier_name,
                'teacher_name': record.teacher_name,
                'material': record.material
                }
    return jsonify(code=0, data=res_data)


# 修改数据库中申请信息
def execute_modify_application_POST(record, json_data):
    activity_name = json_data.get('activity_name')  # 修改活动名称
    if activity_name:
        record.activity_name = activity_name
    people_count = json_data.get('people_num')  # 修改参加人数
    if people_count:
        record.people_count = people_count
    date = json_data.get('date')  # 修改使用日期
    if date:
        record.use_date = date
    begin_time = json_data.get('begin_time')  # 修改开始使用的时间
    if begin_time:
        record.begin_time = begin_time
    end_time = json_data.get('end_time')  # 修改结束使用的时间
    if end_time:
        record.end_time = end_time
    request_ = json_data.get('request')  # 修改申请需求
    if request_:
        record.request = request_
    teacher_name = json_data.get('leader_name')  # 修改负责教师姓名
    if teacher_name:
        record.teacher_name = teacher_name
    material = json_data.get('material')  # 修改负责人盖章材料
    if material:
        record.material = material


# 请求方法为POST时
def modify_application_POST(record, json_data):
    # 检查是否要求为撤回预约信息
    is_withdraw = json_data.get('is_withdraw')
    if is_withdraw is None:
        return jsonify(code=-101, data={'error': '缺少is_withdraw参数'})
    if is_withdraw == 1:  # 需要取消该预约，删除该预约信息
        db.session.delete(record)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'error': '数据库异常'})
        return jsonify(code=0, data={'tip': '申请撤销成功'})

    # 检查是否已审核，已审核的预约信息无法修改
    if record.check_status != "待审核":
        return jsonify(code=0, data={'tip': '此申请已审核，无法修改信息'})

    # 修改预约信息
    execute_modify_application_POST(record, json_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(code=101, data={'tip': '数据库异常'})

    return jsonify(code=0, data={'tip': '修改成功'})


@student.route('/<string:apply_id>', methods=['GET', 'POST'])
def apply_for_stu(apply_id):
    # 在数据库中查找此申请记录
    record = Apply.query.get(apply_id)
    if record is None:
        return jsonify(code=-102, data={'tip': '无此申请记录'})

    # 请求方法为GET时
    if request.method == 'GET':
        return application_GET(record)
    # 请求方法为POST时
    else:
        json_data = request.get_json(silent=True)
        if json_data is None:
            return jsonify(code=-101, data=None)
        return modify_application_POST(record, json_data)