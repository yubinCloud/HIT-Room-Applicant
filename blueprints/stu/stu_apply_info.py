from flask import Blueprint, request, jsonify

from hitapply.models import Apply
from hitapply.extensions import db


stu_apply_info = Blueprint('stu_apply_info', __name__)


# 请求方法为GET时
def apply_for_stu_GET(record):
    # 从数据库中取出相应数据
    res_data = {'room_name': record.room_name,
                'building': record.building,
                'floor': record.floor,
                'activity_name': record.activity_name,
                'people_count': record.people_count,
                'applicant_id': record.applicant_id,
                'applicant_name': record.applicant_name,
                'applicant_phone': record.applicant_phone,
                'apply_time': record.apply_time.strftime('%Y-%m-%d'),
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
def modify_apply_info(record, json_data):
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
def apply_for_stu_POST(record, json_data):
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
            return jsonify(code=101, data={'tip': '数据库异常'})
        return jsonify(code=0, data={'tip': '申请撤销成功'})

    # 检查是否已审核，已审核的预约信息无法修改
    if record.check_status != "待审核":
        return jsonify(code=0, data={'tip': '此申请已审核，无法修改信息'})

    # 修改预约信息
    modify_apply_info(record, json_data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(code=101, data={'tip': '数据库异常'})

    return jsonify(code=0, data={'tip': '修改成功'})


# GET：查看申请详情
# POST：修改申请信息
@stu_apply_info.route('/', methods=['GET', 'POST'])
def apply_for_stu(apply_id):
    # 在数据库中查找此申请记录
    record = Apply.query.get(apply_id)
    if record is None:
        return jsonify(code=-102, data={'tip': '无此申请记录'})

    # 请求方法为GET时
    if request.method == 'GET':
        return apply_for_stu_GET(record)
    # 请求方法为POST时
    else:
        json_data = request.get_json(silent=True)
        if json_data is None:
            return jsonify(code=-101, data=None)
        return apply_for_stu_POST(record, json_data)
