from flask import Blueprint, jsonify

from hitapply.models import Administrator


admin_logout = Blueprint('admin_logout', __name__)

@admin_logout.route('', methods = ['POST'])
def Admin_Logout():
    return jsonify(code=0, data={})