from flask import Blueprint, jsonify
from endsrc.extensions import db
from endsrc.models import Notice

notice_del = Blueprint('notice_del', __name__)


@notice_del.route('', methods=['POST'])
# @adm_login_required(get_grades=(1, 2, 3), post_grades=(1, 2))
def Notice_del(notice_id):
    notice = Notice.query.get(notice_id)
    try:
        db.session.delete(notice)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify(code=101, data={'error': '数据库异常'})

    return jsonify(code=0, data={'tip': '删除成功'})
