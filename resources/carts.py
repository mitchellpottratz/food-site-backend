from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from exceptions.resource_access_denied import ResourceAccessDenied

carts = Blueprint('carts', 'carts')


# Ping Route
@carts.route('/ping', methods=['GET'])
def ping():
    return jsonify(
        data={},
        status={
            'code': 200,
            'Resource': 'IM ALIVE!!!!!!'
        }
    )


