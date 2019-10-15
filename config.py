import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ASÖBJVUEGasJÖKN3248NCLScwQB'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

    IMAGE_UPLOADS_BASIC = "app/static/"
    IMAGE_UPLOADS_USER = "userimages/user/"
    IMAGE_UPLOADS_BLOG = "userimages/blog/"
    IMAGE_UPLOADS_TEMP = "userimages/temp/"

    DOWNLOAD_PATH = "download/"
    SECURED_DOWNLOAD_PATH = "app/protected/download/"

#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['Mailsender@mail.com']
    LANGUAGES = ['en', 'de']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    POSTS_PER_PAGE = 25
    ROLES_PER_PAGE = 25

    ROOT_DIR = os.path.dirname(__file__)
    UPLOAD_DIR=os.path.join(ROOT_DIR, 'uploads')
    GALLERY_ROOT_DIR=os.path.join(ROOT_DIR, 'gallery')
    UPLOAD_ALLOWED_EXTENSIONS = (
          'jpg',
          'png',
          'gif',
    )
