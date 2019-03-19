import json

from flask import Response, Blueprint, request
from app import index_translator, rule_translator

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/translate', methods=['POST'])
def translate():
    """
    Translate API
    :param keyword:
    :return:
    """
    assert request.method == 'POST'
    keyword = request.json.get('keyword', '')
    lang_codes = request.json.get('lang_codes', []).split(',')
    try:
        r_result = rule_translator.translate(keyword, lang_codes)
    except Exception as e:
        r_result = str(e)
    result = {'index': index_translator.search(keyword), 'rule': r_result}
    return Response(json.dumps(result))


@api_bp.route('/api/lang_codes')
def lang_codes():
    """
    Get all available language codes
    :return:
    """
    r = {'lang_codes': {}}
    for lang_code in rule_translator.rules.keys():
        r['lang_codes'][lang_code] = rule_translator.rules[lang_code]['meta']['language_name']
    return Response(json.dumps(r))
