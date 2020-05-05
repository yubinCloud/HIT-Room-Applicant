from flask import Blueprint, jsonify, session, request
from extensions import db
from hitapply.models import Notice


notice_del = Blueprint('notice_del', __name__)


@notice_del.route('', methods = ['POST'])
def Notice_del(notice_id):
    account = session.get('admin_login')
    if account is None:
        return jsonify(code=-102, data={"tip": "用户未登录"})

    json_data = request.get_json(silent=True)

    if json_data is None:
        return jsonify(code=-101, data=None)
    notice = Notice.query.get(notice_id=notice_id)
    try:
        db.session.delete(notice)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(code=101, data={'error': '数据库异常'})

    return jsonify(code=0, data={'tip': ''})