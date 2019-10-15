from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_file
from sqlalchemy import or_
import re
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import Role, User, Permission, Usertorole, usertorole, Roletopermission, roletopermission
from app.translate import translate
from app.about import bp


#from bg_worker import worker

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@bp.route('/about', methods=['GET', 'POST'])
#@login_required
def about():
    return render_template('about/about.html',  title=_('About'), about=about)

@bp.route('/contact', methods=['GET', 'POST'])
#@login_required
def contact():
    return render_template('about/contact.html',  title=_('Contact'), about=contact)
