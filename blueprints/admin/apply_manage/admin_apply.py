from flask import Blueprint, jsonify, request, session
from datetime import datetime

from common.utils import adm_login_required, send_json, record_exception
from models import Apply, Administrator
from extensions import db
from sqlalchemy import and_


admin_apply = Blueprint('admin_apply', __name__)


@admin_apply.route('/room', methods=['GET'])
def look_room_status():
    """
    查看教室状态
    :return:
    """
    rev_json = request.args
    look_date, look_building = rev_json.get('date'), rev_json.get('building')

    if look_date is None or look_building is None:
        return send_json(-101, '缺少必要参数')

    apply_records = Apply.query.filter(and_(Apply.use_date == look_date, Apply.building == look_building)).all()

    result_data = dict()
    for one_apply in apply_records:
        if one_apply.room_name not in result_data.keys():
            result_data[one_apply.room_name] = list()
        result_data[one_apply.room_name].append({
            'begin_time': one_apply.begin_time,
            'end_time': one_apply.end_time,
            'activity': one_apply.activity_name,
            'organization': one_apply.applicant_name
        })

    return send_json(0, result_data)


@admin_apply.route('', methods=['GET', 'POST'])
def acquire_apply_list():
    """
    GET：获取申请列表
    POST：修改申请列表
    :return:
    """
    # 当 method 为 GET 时
    if request.method == 'GET':
        rev_json = request.args
        apply_status_type = rev_json.get('type')
        if apply_status_type is None:
            return send_json(-101, '缺少必要参数')
        apply_records = Apply.query.filter(Apply.check_status == apply_status_type)

        building = rev_json.get('building')
        if building is not None:
            apply_records = apply_records(Apply.building == building)

        apply_records = apply_records.all()

        result_data = [{
            'activity': apply_record.activity_name,
            'organization': apply_record.applicant_name,
            'time': apply_record.apply_time,
            'building': apply_record.building,
            'room_name': apply_record.room_name
        } for apply_record in apply_records]

        return send_json(0, result_data)

    # 当 method 为 POST 时
    else:
        rev_json = request.get_json(silent=True)
        if rev_json is None:
            return send_json(-101, '缺少必需参数')
        apply_list = rev_json.get('apply')
        if type(apply_list) is not list:
            return send_json(-101, '缺少必需参数')
        if len(apply_list) == 0:
            return send_json(0, '待修改列表数据为空')

        admin = Administrator.query.get(session.get('username'))


        success_list = list()
        for one_apply in apply_list:
            activity_name = one_apply.get('activity_name')
            use_date = one_apply.get('date')
            begin_time = one_apply.get('begin_time')
            end_time = one_apply.get('end_time')
            room_name = one_apply.get('room_num', '不指定')
            building = one_apply.get('building', '不指定')
            floor = one_apply.get('floor', '不指定')
            applicant_name = one_apply.get('applicant_name')
            applicant_phone = one_apply.get('applicant_phone')
            if None in {activity_name, use_date, begin_time, end_time, applicant_phone, applicant_name}:
                return send_json(-101, '缺少必需参数')
            one_apply_record = Apply(apply_id=0, activity_name=activity_name, applicant_id='',
                                     applicant_name=applicant_name, applicant_phone=applicant_phone,
                                     apply_time=datetime.now(), use_date=use_date, begin_time=begin_time,
                                     end_time=end_time, people_count=-1, room_name=room_name,
                                     building=building, floor=floor, teacher_name='', check_status='审核通过',
                                     org=admin.org, verifier_name=admin.name)
            db.session.add(one_apply_record)
            try:
                db.session.commit()
                success_list.append(one_apply)
            except Exception as e:
                db.session.rollback()
                record_exception(e)
        return send_json(0, success_list)





@admin_apply.route('/<string:apply_id>', methods=['GET', 'POST'])
def apply_detail(apply_id):
    # GET:
    if request.method == 'GET':
        apply = Apply.query.get(apply_id)
        if apply is None:
            return send_json(-102, '查询不到该申请')
        result_data = {
            'room_num': apply.room_name,
            'applicant': apply.applicant_id,
            'applicant_name': apply.applicant_name,
            'begin_time': apply.begin_time,
            'end_time': apply.end_time,
            'request': apply.request,
            'check_status': apply.check_status,
            'note': apply.note,
            'verifier_name': apply.verifier_name,
            'teacher_name': apply.teacher_name,
            'material': apply.material,
            'org': apply.org,
            'building': apply.building,
            'floor': apply.floor,
            'room_name': apply.room_name
        }
        return send_json(0, result_data)

    # POST:
    else:
        rev_json = request.get_json(silent=True)
        verifier_id, is_pass = rev_json.get('verifier_id'), rev_json.get('is_pass')
        if verifier_id is None or is_pass is None:
            return send_json(-101, '缺少必要参数')
        if is_pass not in {0, 1, 2}:
            return send_json(-102, 'is_pass参数不符合要求')

        admin_account = session.get('admin_login')  # 经adm_login_required装饰器验证后，登录的管理员一定存在
        cur_admin = Administrator.query.get(admin_account)

        apply = Apply.query.get(apply_id)
        if apply is None:
            return send_json(-102, '查询不到该教室')

        apply.verifier_name = cur_admin.name
        apply.org = cur_admin.org
        apply.check_status = {
            0: '审核通过', 1: '审核失败', 2: '待审核'
        }.get(is_pass)

        for k, v in rev_json.items:
            if k in ('note', 'building', 'floor', 'room_name'):
                apply.__setattr__(k ,v)

        try:
            db.session.commit()
        except Exception as e:
            record_exception(e)
            return send_json(101, '数据库异常')
        return send_json(0, {'tip': '审批成功'})





