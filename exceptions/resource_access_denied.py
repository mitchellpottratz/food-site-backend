from flask import jsonify

'''
This exception is thrown when a user tried to access a resource they do not have the rights to
'''

class ResourceAccessDenied(Exception):

    def __init__(self):
        pass

    def get_json_response(self):
        return jsonify(
            data={},
            status={
                'code': 403,
                'message': 'Resource access denied.'
            }
        )







