from flask import Blueprint

main = Blueprint('main', __name__)

# Avoid circular dependencies errors, import after 'main'
from . import views
from . import errors
