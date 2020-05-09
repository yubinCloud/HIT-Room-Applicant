from flask import Blueprint, jsonify, request
from models import Administrator
from hitapply.extensions import db
from hitapply.common.functions import adm_login_required

admin_modify = Blueprint('admin_modify', __name__)


@admin_modify.route('', methods=['POST'])
# @adm_login_required(post_grades=1)
def Admi_modify():
    # 获取json
    rev_json = request.get_json(silent=True)
    type_, account_ = rev_json.get('type'), rev_json.get('account')
    if type_ is None or account_ is None:
        return jsonify(code=-101, data={'tip:': '缺少必须参数'})
    if type_ not in ['delete', 'update']:
        return jsonify(code=-102, data={'tip': 'type参数格式错误'})
    record = Administrator.query.get(account_)
    if type_ == 'delete':  # 删除该账号
        db.session.delete(record)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'tip': '数据库异常'})
        return jsonify(code=0, data={'tip': '删除账号成功'})
    if type_ == 'update':  # 修改账号
        code, tip = modify_admin(record, rev_json)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'error': '数据库异常'})
        return jsonify(code=code, data={'tip': tip})


def modify_admin(record, rev_json):
    '''
    修改数据库相应字段
    :param record: 数据库Administrator实例
    :param rev_json: 接受的json数据
    :return: (0, '修改账号成功')
    '''
    # 修改数据库相应字段
    password_, grade_, name_, phone_, org_ = rev_json.get('password'), rev_json.get('grade'), \
                                             rev_json.get('name'), rev_json.get('phone'), \
                                             rev_json.get('org')
    if password_:
        record.password = password_
    if grade_:
        record.grade = grade_
    if name_:
        record.name = name_
    if phone_:
        record.phone = phone_
    if org_:
        record.org = org_
    return 0, '修改账号成功'
