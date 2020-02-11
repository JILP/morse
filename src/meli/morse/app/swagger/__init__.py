from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/translate/v1/api/docs'
API_URL = '/static/translate_swagger.json'


swagger = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Morse Translator"
    }
)
