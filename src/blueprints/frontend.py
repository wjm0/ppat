from flask import Response, Blueprint, request

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """
    Response the index page HTML

    :return:
    """
    return Response('index.html')
