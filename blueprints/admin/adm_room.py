from flask import Blueprint, jsonify, request
from hitapply.common.functions import adm_login_required

adm_room = Blueprint('adm_room', __name__)


@adm_room.route('', methods=['GET', 'POST'])
@adm_login_required(get_grades=(1, 2, 3), post_grades=(1, 2, 3))
def Adm_room():
    pass
