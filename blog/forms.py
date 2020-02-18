from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from blog.models import User
from flask_login import current_user
from blog import crypt

class RegistrationForm(FlaskForm):

    username = StringField('Username:', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one.')

    
    # def __repr__(self):
    #     return "'Username: '{}, 'Email: '{}".format(self.username, self.email)


class LoginForm(FlaskForm):

    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log in')
    remember = BooleanField('Remember me:')


class SearchForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
    submit = SubmitField('Search')

class UpdateForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Old Password:', validators=[DataRequired()])
    new_password = PasswordField('New Password:', validators=[
                                     DataRequired()])
    confirm_password = PasswordField('Confirm New Password:', validators=[
        DataRequired(), EqualTo('new_password')])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Update')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one')
    
    def validate_password(self, password):
        if password.data == current_user.password:
            user = User.query.filter_by(username=self.email.data).first()
            if crypt.generate_password_hash(password.data).decode('utf-8') != user.password:
                raise ValidationError('Your old password is incorrect. Please try again')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no accoutn with that email. You must register first.')
    


class ResetPasswordFrom(FlaskForm):
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', validators=[
                                     DataRequired(), EqualTo('password')])
                                     
    submit = SubmitField('Reset password')
