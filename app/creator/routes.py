from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.creator import bp
from app.creator.forms import Form_Creator
from app.models import User, Charactersheet, Abilities


@bp.route('/index', methods=['GET', 'POST'])
def creator_index():
    collection = db.session.query(Charactersheet).limit(5).all()
    return render_template('creator/index.html', title=_('Sign In'), data=collection)


@bp.route('/collection', methods=['GET', 'POST'])
def creator_collection():
    collection = db.session.query(Charactersheet).all()
    return render_template('creator/collection.html', title=_('Sign In'), data=collection)

@bp.route('/download', methods=['GET', 'POST'])
def creator_download():

    return render_template('creator/download.html', title=_('Sign In'))

@bp.route('/create', methods=['GET', 'POST'])
def creator_create():
    form = Form_Creator()
    return render_template('creator/creator.html', title=_('Sign In'), form=form)
