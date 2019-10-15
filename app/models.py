from datetime import datetime, timedelta
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from sqlalchemy.dialects.mysql import INTEGER
from app import db, login

class boardgamelist(UserMixin, db.Model):
    __tablename__ = 'boardgamelist'
    id = db.Column(db.Integer, primary_key=True, unique = True)
    name = db.Column(db.String(120))
    bgg_id = db.Column(db.String(80))
    extension = db.Column(db.Integer,db.ForeignKey('boardgamelist.id'))
    image_resource = db.Column(db.String(160))
    player_min=db.Column(db.Integer)
    player_best=db.Column(db.Integer)
    player_max=db.Column(db.Integer)
    time_min=db.Column(db.Integer)
    time_max=db.Column(db.Integer)
    time_avg=db.Column(db.Integer)
    lastplayed=db.Column(db.DateTime, default=datetime.utcnow)
    owner_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default = 1)

    def __repr__(self):
        return '<Boardgame: {} -> bgg_id: {} owner_id_fk:{} > <{} {} {}>'.format(self.name, self.bgg_id, self.owner_id_fk, self.player_min, self.player_max, self.player_best)

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class Polloption(db.Model):
    __tablename__ = 'polloption'
    id = db.Column(db.Integer, primary_key=True, unique = True)
    poll = db.Column(db.Integer, db.ForeignKey('poll.id'))
    #options = db.Column(db.Integer, db.ForeignKey('boardgamelist.id'))
    vote = db.Column(db.Integer())
    participant = db.Column(db.Integer, db.ForeignKey('user.id'))
    #votetime = db.Column(db.DateTime, default=datetime.utcnow)

class Poll(db.Model):
    __tablename__ = 'poll'
    id = db.Column(db.Integer, primary_key=True, unique = True)
    title = db.Column(db.Text, default = "title")
    created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    event = db.Column(db.Integer, db.ForeignKey('event.id'))
    chosen = db.Column(db.Integer)
    votes = db.relationship('Polloption', backref='masterpoll')


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, unique = True)
    name = db.Column(db.Text, default = "event")
    type = db.Column(db.String(120), default="common")
    event_comment =  db.Column(db.Text, default = "A classic boardgame evening")
    event_image =  db.Column(db.Text, default = "userimage/event/default.jpg")
    main_text = db.Column(db.Text, default="Event description")
    sub_text = db.Column(db.Text, default="Further information")
    location = db.Column(db.Text, default="t.b.a.")
    dateofevent = db.Column(db.DateTime, default=datetime.utcnow)
    max_player = db.Column(db.Integer)
    max_games = db.Column(db.Integer)
    player = db.relationship('User', backref='eventparticipant')
    eventpoll = db.relationship('Poll', backref='masterevent')
    #games = db.relationship('boardgamelist', backref='eventgames') # has to be replaced by a poll???
    player_comments = db.relationship('Comment', backref='parentevent', lazy='dynamic')
    event_host = db.Column(db.Integer, db.ForeignKey("user.id"))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event = db.Column(db.Integer, db.ForeignKey('event.id'))
    category = db.Column(db.String(100))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Comment {}>'.format(self.body)

class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    category = db.Column(db.String(150))
    title = db.Column(db.String(150))
    text = db.Column(db.String(800))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    image_name = db.Column(db.String(200), default="defaultavatar.jpg")
    #liked = db.relationship('User', backref='liked')
    #downloads = db.relationship('Download', backref='blogentry')

class Download(db.Model):
    __tablename__ = 'download'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(150), index=True, unique=True)
    path = db.Column(db.String(254), index=True, unique=True)
    category = db.Column(db.String(150))
    subfolder = db.Column(db.String(150))
    description = db.Column(db.Text, default="description")
    loadcount = db.Column(db.Integer, default = 0)
    right_to_download = db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
    entry_image =  db.Column(db.Text, default = "img/icon_book.png")
    #blog = db.Column("user_id", db.Integer, db.ForeignKey("Blog.id"))

class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    permissionname = db.Column(db.String(64), index=True, unique=True)
    action = db.Column(db.String(254), index=True, unique=True)

class Roletopermission(object):
    """
    Roletopermission object the "roletopermission" table.
    """
    def __init__(self, role_id, permission_id):
        self.role_id = role_id
        self.permission_id = permission_id

roletopermission = db.Table("roletopermission",
                      db.metadata,
                      db.Column("id", db.Integer, primary_key=True),
                      db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
                      db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
                      )
db.mapper(Roletopermission, roletopermission)
db.Index("roletopermission_index", roletopermission.c.role_id, roletopermission.c.permission_id, unique=True)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(64), index=True, unique=True)
    permission = db.relationship("Permission",
                     secondary=roletopermission,
                    backref=db.backref("Role", lazy="dynamic"),)

class Usertorole(object):
    """
    Dogs object the "dogs" table.
    """
    def __init__(self, role_id, user_id):
        self.role_id = role_id
        self.user_id = user_id

usertorole = db.Table("usertorole",
                      db.metadata,
                      db.Column("id", db.Integer, primary_key=True),
                      db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                      db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
                      )

db.mapper(Usertorole, usertorole)
db.Index("usertorole_index", usertorole.c.user_id, usertorole.c.role_id, unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    approved = db.Column(db.Boolean, default = False)
    login_tries = db.Column(db.Integer, default = 0)
    account_suspended = db.Column(db.Boolean, default = False)
    real_name = db.Column(db.String(200), default="Nobody")
    image_name = db.Column(db.String(200), default="defaultavatar.jpg")
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    blog = db.relationship('Blog', backref='author', lazy='dynamic')
    downloads = db.relationship('Download', backref='author', lazy='dynamic',cascade="all,delete")
    comments = db.relationship('Comment', backref='author', lazy=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
                               )

    role = db.relationship("Role",
                     secondary=usertorole,
                    backref=db.backref("User", lazy="dynamic"),)

    #plays = db.relationship('plays', backref='player', lazy=True)

    def check_permission(self, permission_to_check):
        print(permission_to_check)
        if self.is_anonymous:
            curr_user = User.query.filter(User.username=="Guest").first()
        else:
            curr_user = self
        count = Permission.query.outerjoin(Roletopermission, Roletopermission.permission_id == Permission.id).outerjoin(Role, Role.id == Roletopermission.role_id).outerjoin(Usertorole, Usertorole.role_id == Role.id).filter(Usertorole.user_id==curr_user.id).filter(Permission.action==permission_to_check).count()
        if count >= 1:
            return True
        return False

    def get_permissions(self):
        roles = Role.query.count()
        #roles = User.query.filter(Usertorole.user_id==self.id).outerjoin(Usertorole, Usertorole.user_id == self.id).outerjoin(Roletopermission, Roletopermission.role_id == Usertorole.role_id).all()
        #permissionlist=Role.query.join(Usertorole, Usertorole.role_id==Role.id).filter(Usertorole.user_id==self.id).all()
        roles = Permission.query.outerjoin(Roletopermission, Roletopermission.permission_id == Permission.id).outerjoin(Role, Role.id == Roletopermission.role_id).outerjoin(Usertorole, Usertorole.role_id == Role.id).filter(Usertorole.user_id==self.id).all()
        for entry in roles:
            print(self.id, entry.id)
        #permissionlist=Role.query.outerjoin(Usertorole, Usertorole.user_id==self.id).outerjoin(Roletopermission, Roletopermission.permission_id == Permission.id).all()
        return roles

    def get_role(self):
        rolelist=Role.query.join(Usertorole, Usertorole.role_id==Role.id).filter(Usertorole.user_id==self.id).all()
        return rolelist


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
            self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

@staticmethod
def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, current_app.config['SECRET_KEY'],
                        algorithms=['HS256'])['reset_password']
    except:
        return
    return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
