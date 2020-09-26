from flask import Blueprint, jsonify

from models import Notice

notice_info = Blueprint('notice_info', __name__)

@notice_info.route('', methods = ['GET'])
def Notice_Info(notice_id):
    if notice_id == 0:
        length = len(Notice.query.all())
        record = Notice.query.get(length)
        if record is None:
            return jsonify(code=-102, data={notice_id})
        else:
            data = {
                'id': record.notice_id,
                'org': record.org,
                'title': record.title,
                'time': record.time.strftime('%Y-%m-%d'),
                "content": record.content
            }
            return jsonify(code=0, data=data)
    else:
        record = Notice.query.get(notice_id)
        if record is None:
            return jsonify(code = -102, data = {notice_id})
        else:
            data = {
                'id': record.notice_id,
                'org': record.org,
                'title': record.title,
                'time': record.time.strftime('%Y-%m-%d'),
                "content": record.content
            }
            return jsonify(code=0, data=data)