from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


def register_blueprints():
    from blueprints.frontend import frontend_bp
    from blueprints.api import  api_bp

    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp)


register_blueprints()
