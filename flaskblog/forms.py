from flask_wtf import FlaskForm
from wtforms import StringField ,TextAreaField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flaskblog.models import *
from flask_wtf.file import FileField, FileRequired, FileAllowed

class SignupForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min=3,max=50)])
    email = StringField('Email', validators =[DataRequired(), Email()])
    password = PasswordField('Password',validators =[DataRequired(), Length(min=5,max=50)] )
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    picture = FileField('Upload profile picture',validators=[FileAllowed(['jpg', 'png'])])
    submit= SubmitField('signup')
    def validate_username(self, username):
    	user = User.query.filter_by(username=username.data).first()
    	if user:
    		raise ValidationError('This username has been taken. Try another.')
    		
    def validate_email(self, email):
    	user = User.query.filter_by(email=email.data).first()
    	if user:
    		raise ValidationError('This email has been taken. Try another.')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title',validators =[Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')