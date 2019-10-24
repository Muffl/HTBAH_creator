from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, FloatField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User


class Form_Creator(FlaskForm):
    name = StringField(_l('Username'), validators=[DataRequired()],render_kw={"placeholder": "Charaktername"})
    sex = RadioField(_l('Sex'), choices=[('m','männlich'),('f','weiblich'),('x','divers')], validators=[DataRequired()])
    image = StringField(_l('Image'),render_kw={"placeholder": "Ein Characterbild"})
    job = StringField(_l('Job'), validators=[DataRequired()],render_kw={"placeholder": "Beruf"})
    age = IntegerField(_l('age'), validators=[DataRequired()],render_kw={"placeholder": "Alter"})
    size = FloatField(_l('Size'), validators=[DataRequired()],render_kw={"placeholder": "Größe in cm"})

    KK = IntegerField(_l('KK'), validators=[DataRequired()],render_kw={"placeholder": "Körperkraft"})
    AU = IntegerField(_l('AU'), validators=[DataRequired()],render_kw={"placeholder": "Ausdauer"})
    GE = IntegerField(_l('GE'), validators=[DataRequired()],render_kw={"placeholder": "Geschicklichkeit"})
    IN = IntegerField(_l('IN'), validators=[DataRequired()],render_kw={"placeholder": "Intelligenz"})
    CH = IntegerField(_l('CH'), validators=[DataRequired()],render_kw={"placeholder": "Charisma"})
    MB = IntegerField(_l('MB'), validators=[DataRequired()],render_kw={"placeholder": "Mentale Belastbarkeit"})
    ATN = IntegerField(_l('ATN'), validators=[DataRequired()],render_kw={"placeholder": "Attacke Nahkampf"})
    PA = IntegerField(_l('PA'), validators=[DataRequired()],render_kw={"placeholder": "Parade"})
    ATD = IntegerField(_l('ATD'), validators=[DataRequired()],render_kw={"placeholder": "Attacke Fernkampf"})
    INI = IntegerField(_l('INI'), validators=[DataRequired()],render_kw={"placeholder": "Initiative"})
    LE = IntegerField(_l('LE'), validators=[DataRequired()],render_kw={"placeholder": "Lebensenergie"})
    GG = IntegerField(_l('GG'), validators=[DataRequired()],render_kw={"placeholder": "Geistige Gesundheit"})

    itemselect = SelectField(_l('item'), choices=[('other','0')])
    probeselect1 = SelectField(_l('item'), choices=[('other','0')])
    probeselect2 = SelectField(_l('item'), choices=[('other','0')])
    probeselect3 = SelectField(_l('item'), choices=[('other','0')])
    value = IntegerField(_l('age'))

    submit = SubmitField(_l('Sign In'))
