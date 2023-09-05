from flask import Blueprint

admin_app = Blueprint('admin', __name__)

from admin import routes,login,servicios,productos,tipo_productos,usuarios