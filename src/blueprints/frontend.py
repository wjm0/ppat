from flask import Blueprint, render_template

from app import rule_translator

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def index():
    """
    Response the index page HTML

    :return:
    """
    lang_codes = {}
    for lang_code in rule_translator.rules.keys():
        lang_codes[lang_code] = rule_translator.rules[lang_code]['meta']['language_name']
    return render_template('index.html', lang_codes=lang_codes)
