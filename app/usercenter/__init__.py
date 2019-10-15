from flask import Blueprint

bp = Blueprint('usercenter', __name__)

from app.usercenter import routes
