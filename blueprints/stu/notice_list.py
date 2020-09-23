from flask import Blueprint, jsonify, request
from models import Notice

notice_list = Blueprint('notice_list', __name__)


@notice_list.route('', methods=['GET'])
def Notice_List():
    start_id = request.args.get('startid')
    end_id = request.args.get('endid')
    data = []
    record = Notice.query.order_by(Notice.time.desc()).slice(int(start_id), int(end_id) + 1).all()

    if record is None:
        return jsonify(error_code=-102, data={})

    for i in record:
        temp = {
            'id': i.notice_id,
            'org': i.org,
            'title': i.title,
            'time': i.time.strftime('%Y-%m-%d')
        }
        data.append(temp)
    return jsonify(code=0, data=data)
