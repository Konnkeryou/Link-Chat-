from ast import Pass, Sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import InputRequired, length, EqualTo, ValidationError

from models import User

def invalid_credentials(form, field):
    #creditials checker 

    username_used = form.username.data 
    password_used = field.data

    user_object = User.query.filter_by(username=username_used).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif password_used != user_object.password:
        raise ValidationError("Username or password is incorrect")


class RegistrationForm(FlaskForm):
    #registration 

    username = StringField('username_tag', validators=[InputRequired(message= "Username required")])
    password = PasswordField ('password_tag', validators=[InputRequired(message="Password required"), length(min=8, max=16, message="Password must be between 8 and 16 characters")])
    confirm_password = PasswordField ('confirm_tag',validators=[InputRequired(message="Password required"), EqualTo ('password', message="Password must match")]) 
    submit_button = SubmitField('Register')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError ("Username in used, select a diffirent name")

class loginForm (FlaskForm):
     # login form

    username = StringField('username_tag', validators= [InputRequired(message="Username required")])
    password = PasswordField('password_tag', validators= [InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('login')
