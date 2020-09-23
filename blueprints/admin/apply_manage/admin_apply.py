from flask import Blueprint, jsonify, request

from common.utils import adm_login_required, send_json, record_exception
from models import Apply
from extensions import db
from sqlalchemy import and_


admin_apply = Blueprint('admin_apply', __name__)


@admin_apply.route('/room', methods=['GET'])
def look_room_status():
    """
    查看教室状态
    :return:
    """
    rev_json = request.get_json(silent=True)
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
    rev_json = request.get_json(silent=True)

    if request.method == 'GET':
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

    else:
        pass



