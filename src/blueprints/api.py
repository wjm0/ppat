from flask import Response, Blueprint, request


from app import index_translator

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/translate')
def translate(keyword):
    result = {'index':index_translator.search(keyword), 'algorithm':{}}

    return Response(result)


@api_bp.route('/api/lang_codes')
def lang_codes():
    """
    Get all available language codes
    :return:
    """
    return Response()
