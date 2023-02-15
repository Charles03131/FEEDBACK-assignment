from flask_wtf import FlaskForm

from wtforms import StringField,PasswordField,IntegerField,TextAreaField
from wtforms.validators import InputRequired,Length,Email



class RegisterUser(FlaskForm):
    """form for registering a user"""


    username=StringField('username',validators=[InputRequired(),Length(min=1,max=20)])    # 20 or less char
    password=PasswordField('password',validators=[InputRequired(),Length(min=5,max=55)])              
    email=StringField('email',validators=[InputRequired(),Email(),Length(max=50)])   #50 char or less
    firstname=StringField('firstname',validators=[InputRequired(),Length(max=30)])     #30 or less char
    lastname=StringField('lastname',validators=[InputRequired(),Length(max=30)])    #30 or less char





class LogInForm(FlaskForm):
    """form for logging in a user"""

    username=StringField('username',validators=[InputRequired(),Length(min=1,max=20)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=5,max=55)])



class FeedbackForm(FlaskForm):
    """form for feedback post"""

    title=StringField('title',validators=[InputRequired()])
    content=TextAreaField('content',validators=[InputRequired()])


