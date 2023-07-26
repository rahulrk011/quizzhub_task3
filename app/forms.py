from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,IntegerField,HiddenField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length,NumberRange
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username .')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username .')
        
class EditProfileForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    about_me= TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username as it alreaady EXISTS.')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post= TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit= SubmitField('Submit')

class quiz_info_Form(FlaskForm):
    name=StringField('Name of Quiz',validators=[DataRequired()])
    noq=IntegerField('Number of Questions',validators=[DataRequired(),
        NumberRange(min=1, max=30)])
    submit= SubmitField('Continue') 

class quizForm(FlaskForm):
    question_number=IntegerField('question number',validators=[DataRequired()])
    question=TextAreaField('Question', validators=[DataRequired(), Length(min=1, max=140)])
    op1=StringField('Option 1',validators=[DataRequired()])
    op2=StringField('Option 2',validators=[DataRequired()])
    op3=StringField('Option 3',validators=[DataRequired()])
    op4=StringField('Option 4',validators=[DataRequired()])
    crctop=IntegerField('Correct Option',validators=[DataRequired()])