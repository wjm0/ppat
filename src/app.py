from flask import Flask
from flask_caching import Cache

from translators.translator import IndexTranslator, AlgorithmTranslator

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

index_translator = IndexTranslator()
algorithm_translator = AlgorithmTranslator()


def register_blueprints():
    from blueprints.frontend import frontend_bp
    from blueprints.api import  api_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp)


register_blueprints()
