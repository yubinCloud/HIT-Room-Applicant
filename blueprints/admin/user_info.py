from flask import Blueprint, jsonify

from hitapply.models import Administrator


user_info = Blueprint('user_info', __name__)

@user_info.route('', methods = ['GET'])
def User_Info():
    return jsonify(code=0, data={})