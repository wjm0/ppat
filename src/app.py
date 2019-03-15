from flask import Flask

from translators.translator import IndexTranslator, RuleTranslator

app = Flask(__name__)

index_translator = IndexTranslator()
rule_translator = RuleTranslator()


def register_blueprints():
    from blueprints.frontend import frontend_bp
    from blueprints.api import  api_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp)


register_blueprints()
