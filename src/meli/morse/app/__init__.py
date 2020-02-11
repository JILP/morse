import flask
from flask_bootstrap import Bootstrap

from meli.morse.config import config
from .api import api as api_blueprint
from .main import main as main_blueprint
from .swagger import swagger as swagger_blueprint
from .swagger import SWAGGER_URL

bootstrap = Bootstrap()


def create_app(config_name):
    app = flask.Flask(__name__)
    app.config.from_object(config(config_name))
    config(config_name).init_app(app)

    bootstrap.init_app(app)

    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/translate/v1')
    

    # attach routes and custom error pages here
    return app

