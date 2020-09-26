from flask import Blueprint, request

from common.utils import adm_login_required, send_json, record_exception
from models import Timetable
from extensions import db


admin_timetable = Blueprint('admin_timetable', __name__)


@admin_timetable.route('', methods=['GET', 'POST'])
def adm_timetable_handler():
    """
    GET：查看时间表
    POST: 修改时间表
    :return:
    """
    if request.method == 'GET':
        records = Timetable.query.all()
        result_data = [['第{}节'.format(record.class_id), record.begin_time, record.end_time]
                       for record in records]
        return send_json(0, result_data)

    # 当 method 为 POST 时
    else:
        new_timetable = request.get_json(silent=True).get('timetable_manage')
        if new_timetable is None:
            return {-101, '缺少必要参数'}

        # 删除旧时间表
        old_timetable = Timetable.query.all()
        for klass in old_timetable:
            db.session.delete(klass)
        # 加入新时间表
        for klass in new_timetable:
            new_record = Timetable(klass[0], klass[1], klass[2])
            db.session.add(new_record)
        # 提交到数据库
        try:
            db.session.commit()
        except Exception as e:
            record_exception(e)
            return send_json(101, '数据库异常')
        return send_json(0, {'tip': '更新成功'})

