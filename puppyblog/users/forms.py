from puppyblog.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from flask_wtf.file import FileField, FileAllowed

def email_exists(form, field):
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError('Email Already Exists')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(3, 15, message='Between 3 to 15 characters')])
    email = StringField('E-mail', validators=[DataRequired(), Email(), email_exists])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(5), EqualTo('confirm', message='Password must match')])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Register')


class UpdateUserForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email(), email_exists])
    name = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_loggedin = BooleanField('Stay logged-in')
    submit = SubmitField('LogIn')