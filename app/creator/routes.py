from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.creator import bp
from app.creator.forms import *
from app.models import User


@bp.route('/index', methods=['GET', 'POST'])
def creator_index():
    form = LoginForm()

    return render_template('creator/index.html', title=_('Sign In'), form=form)


@bp.route('/collection', methods=['GET', 'POST'])
def creator_collection():
    form = LoginForm()

    return render_template('creator/login.html', title=_('Sign In'), form=form)

@bp.route('/download', methods=['GET', 'POST'])
def creator_download():
    form = LoginForm()

    return render_template('creator/login.html', title=_('Sign In'), form=form)

@bp.route('/create', methods=['GET', 'POST'])
def creator_create():
    form = LoginForm()

    return render_template('creator/login.html', title=_('Sign In'), form=form)
