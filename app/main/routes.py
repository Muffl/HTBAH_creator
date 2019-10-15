from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from sqlalchemy import or_
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import *
from app.main import bp


from flask import request, redirect
import os, hashlib
from werkzeug import secure_filename
from external.imageupload import func_import_image



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/upload-image/<target>/<user>', methods=['GET', 'POST'])
@bp.route('/upload-image/<target>', defaults={'user':'nix'} , methods=['GET', 'POST'])
def upload_image(target, user):
    if request.method == "POST":
        if request.files:
            func_import_image(target, user, request.files)
    return render_template("upload.html", target=target, user=user)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    events = db.session.query(db_event).all()
    blog = db.session.query(db_blog).filter(db_blog.category != 'title').all()
    news = db.session.query(db_blog).filter(db_blog.category == 'news').order_by(db_blog.created_date.desc()).all()
    titleshow = db.session.query(db_blog).filter(db_blog.category == 'title').all()
    page = request.args.get('page', 1, type=int)
    return render_template('index.html',
                    title=_('Home'),
                    blog=blog,
                    news=news,
                    titleshow = titleshow,
                    events=events[:3]
                    )



@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})
