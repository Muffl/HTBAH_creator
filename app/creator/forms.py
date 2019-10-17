from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User


class Form_Creator(FlaskForm):
    name = StringField(_l('Username'), validators=[DataRequired()])
    sex = RadioField(_l('Sex'), choices=[('m','m'),('f','f'),('x','x')], validators=[DataRequired()])
    job = StringField(_l('Job'), validators=[DataRequired()])
    age = IntegerField(_l('age'), validators=[DataRequired()])
    size = FloatField(_l('Size'), validators=[DataRequired()])

    KK = IntegerField(_l('KK'), validators=[DataRequired()])
    AU = IntegerField(_l('AU'), validators=[DataRequired()])
    GE = IntegerField(_l('GE'), validators=[DataRequired()])
    IN = IntegerField(_l('IN'), validators=[DataRequired()])
    CH = IntegerField(_l('CH'), validators=[DataRequired()])
    MB = IntegerField(_l('MB'), validators=[DataRequired()])
    ATN = IntegerField(_l('ATN'), validators=[DataRequired()])
    PA = IntegerField(_l('PA'), validators=[DataRequired()])
    ATD = IntegerField(_l('ATD'), validators=[DataRequired()])
    INI = IntegerField(_l('INI'), validators=[DataRequired()])
    LE = IntegerField(_l('LE'), validators=[DataRequired()])
    GG = IntegerField(_l('GG'), validators=[DataRequired()])

    submit = SubmitField(_l('Sign In'))
