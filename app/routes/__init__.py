from app import app

from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin', static_folder='static')
roommate_bp = Blueprint('roommate', __name__, template_folder='templates/roommate', static_folder='static')
family_member_bp = Blueprint('family_member', __name__, template_folder='templates/family_member', static_folder='static')


from . import user

app.register_blueprint(admin_bp, url_prefix='/admin')
# app.register_blueprint(user_bp, url_prefix="/parent")