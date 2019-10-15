from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User

class form_edit_profile(FlaskForm):
    username = StringField(_l('Username'))
    email = StringField(_l('Email'))
    name = StringField(_l('Name'))
    submit = SubmitField(_l('Submit'))

class form_edit_role(FlaskForm):
    rolename = StringField(_l('Role'))
    old_rolename = StringField(_l('Old_Role'))
    submit = SubmitField(_l('Submit'))

class form_edit_role_add_perm(FlaskForm):
    permissiontoadd = SelectField(_l('Permission'), coerce=int)

class form_add_role(FlaskForm):
    roletoadd = StringField(_l('Role'))

class form_edit_permission(FlaskForm):
    permissionname = StringField(_l('Permission Name'))
    permissionaction = StringField(_l('Permission Action'))
    submit = SubmitField(_l('Submit'))

class form_edit_role_for_user(FlaskForm):
    role = SelectField(_l('Role'), coerce=int)
    submit = SubmitField(_l('Submit'))
