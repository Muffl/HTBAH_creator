from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from sqlalchemy import or_
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.models import User, Post, Event as db_event, Blog as db_blog, Download
#from app.translate import translate

import urllib.request
from bs4 import BeautifulSoup
from werkzeug import secure_filename
from flask import request, redirect
import os


def provide_download_link(subfolder):
    print("6:"+subfolder)
    downloadpath = os.path.join(current_app.instance_path, current_app.config["DOWNLOAD_PATH"], subfolder)
    print("7:"+downloadpath)
    return downloadpath

def upload_download(subfolder, request_files, filename):#target, user, source, filename):
    filetoload = request_files["file"]
    #### DEFINE PATH #########
    cwd = os.getcwd()
    uploadfolder = os.path.join(current_app.instance_path, current_app.config["DOWNLOAD_PATH"], secure_filename(subfolder))
    print(uploadfolder)
    #### CREATE PATH ########
    if os.path.isdir(uploadfolder):
        print (uploadfolder)
    else:
        os.mkdir(uploadfolder)
    ###### SAVE IMAGE #######
    file_ending = filetoload.filename.split(".")[-1]
    filetoload.save(os.path.join(uploadfolder, secure_filename(filename+"."+file_ending)))
    return secure_filename(filename+"."+file_ending)


def import_image(target, user, source, filename):

    #### DEFINE PATH #########
    cwd = os.getcwd()
    if target == 'boardgame':
        uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"],current_app.config["IMAGE_UPLOADS_BOARDGAME"], secure_filename(filename))

    #### CREATE PATH ########
    if os.path.isdir(uploadpath):
        print (uploadpath)
    else:
        os.mkdir(uploadpath)

    ###### SAVE IMAGE #######
    try:
        urllib.request.urlretrieve(source, os.path.join(uploadpath, secure_filename('thumbnail.jpg')))
        print(os.path.join(uploadpath, secure_filename('thumbnail.jpg')))
        return os.path.join(current_app.config["IMAGE_UPLOADS_BOARDGAME"], secure_filename(filename),  secure_filename('thumbnail.jpg'))
    except:
        return source


def func_import_image(target, user, request_files):
   image = request_files["image"]
   cwd = os.getcwd()
   uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"], current_app.config["IMAGE_UPLOADS_TEMP"])
   if target == 'temp':
       uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"], current_app.config["IMAGE_UPLOADS_TEMP"])
   if target == 'user':
        cuser = db.session.query(User).filter(User.username==user).first()
        if cuser == None:
            cuser = db.session.query(User).filter(User.id==current_user.id).first()
        if image.filename[-3:].lower() == 'jpg':
            image.filename = 'image.jpg'
        elif image.filename[-3:].lower() == 'png':
            image.filename = 'image.png'
        else:
            image.filename = 'unknown'
            flash('Image could not be verfied. (ONLY .jpg and .png)')
            return redirect(url_for('main.upload_image',target=target, user=user))
        uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"], current_app.config["IMAGE_UPLOADS_USER"], cuser.username)
        cuser.image_name = ("userimages/user/"+cuser.username+"/"+secure_filename(image.filename))
   if target == 'boardgame':
        uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"], current_app.config["IMAGE_UPLOADS_BOARDGAME"])
   if target == 'event':
        uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"], current_app.config["IMAGE_UPLOADS_EVENT"], user)
        if image.filename[-3:].lower() == 'jpg':
            image.filename = 'image.jpg'
        elif image.filename[-3:].lower() == 'png':
            image.filename = 'image.png'
        else:
            image.filename = 'unknown'
            flash('Image could not be verfied. (ONLY .jpg and .png)')
            return redirect(url_for('main.upload_image',target=target, user=user))
   if target == 'blog':
        uploadpath = os.path.join(cwd, current_app.config["IMAGE_UPLOADS_BASIC"], current_app.config["IMAGE_UPLOADS_BLOG"], user)
        print(image.filename[-3:].lower())
        if image.filename[-3:].lower() == 'jpg':
            image.filename = 'image.jpg'
        elif image.filename[-3:].lower() == 'png':
            image.filename = 'image.png'
   if os.path.isdir(uploadpath):
        print (uploadpath)
   else:
        os.mkdir(uploadpath)
   image.save(os.path.join(uploadpath, secure_filename(image.filename)))
   if os.path.exists(os.path.join(uploadpath, secure_filename(image.filename))):
        print("upload successful")
        db.session.commit()
   else:
        print("UPLOAD ERROR")
        db.session.rollback()
   if target == 'user':
        return redirect(url_for('usercenter.usermanagement', username=user))
   if target == 'event':
        cevent=db.session.query(db_event).filter(db_event.id==user).first()
        if db.session.query(db_event).filter(db_event.id==user).count() == 1:
            cevent.event_image="userimages/event/"+str(cevent.id)+"/"+secure_filename(image.filename)
            db.session.commit()
        else:
            flash('Image could not be inserted to database.')
        return redirect(url_for('boardgame.show_event', id=user))
   if target == 'blog':
        cblog=db.session.query(db_blog).filter(db_blog.id==user).first()
        if db.session.query(db_blog).filter(db_blog.id==user).count() == 1:
            cblog.image_name="userimages/blog/"+str(cblog.id)+"/"+secure_filename(image.filename)
            db.session.commit()
        else:
            flash('Image could not be inserted to database.')
        return redirect(url_for('main.index'))
   return redirect(url_for('main.upload_image',target=target, user=user))
