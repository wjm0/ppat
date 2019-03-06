from flask import Response, Blueprint, request

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/translate')
def translate():
    return Response()


@api_bp.route('/api/lang_codes')
def lang_codes():
    """
    Get all available language codes
    :return:
    """
    return Response()
