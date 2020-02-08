from flask import Blueprint

api = Blueprint('api', __name__)

# Avoid circular dependencies errors, import after 'main'
from . import translate
from . import errors
