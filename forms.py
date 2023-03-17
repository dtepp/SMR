from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,BooleanField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


# WTForm
class CreateMajorForm(FlaskForm):
    majorName = StringField("Major Title", validators=[DataRequired()])
    school = StringField("School", validators=[DataRequired()])
    applyReq = StringField("applyReq", validators=[DataRequired()])
    langReq = StringField("langReq", validators=[DataRequired()])
    Fee = StringField("Fee", validators=[DataRequired()])
    course = CKEditorField("Course Content", validators=[DataRequired()])
    cluster =StringField("cluster")
    label = StringField("label")
    submit = SubmitField("Submit Major")
    
    
    
class CreateLevelForm(FlaskForm):
    countryName = StringField("countryName", validators=[DataRequired()])
    schoolname = StringField("School", validators=[DataRequired()])
    isApply = BooleanField("isApply")
    isAddOn = BooleanField("isAddOn")
    schoolscore = StringField("School Score")
    addscore =StringField("addscore")
    submit = SubmitField("Submit Major")
    


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("SIGN ME UP!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("LET ME IN!")


