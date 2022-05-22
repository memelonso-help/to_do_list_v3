from flask_wtf import FlaskForm, RecaptchaField
# flaskform class is the base of all our forms, has csrf protection for session security
from wtforms import TextAreaField, StringField, DateField, BooleanField, SubmitField, SelectField, FormField, PasswordField
# these fields are required in my form thus far
from wtforms.validators import EqualTo, Length, InputRequired, Regexp, Optional
# indicates that the form cannot be submitted without data in the field, and for reconfirming passwords
from flask_wtf.csrf import CSRFProtect
# protect me file using csrf tokens

# i want a signupform, loginform, also create a settings form and set password form using FlaskForm due to protection
# but i guess in general it's best practice to create forms for all my features
# taskfillform, tasklistform, complistform
# recaptcha in signup form

csrf = CSRFProtect()
WTF_CSRF_SECRET_KEY = 'no security'

class signupform(FlaskForm):
    username = StringField("Username", validators = [InputRequired(), Length(min = 1, max = 20, message = "20 char limit")])
    # password = StringField("Password", validators = [InputRequired(), Length(min = 1, max = 20, message = "20 char limit"), Regexp(regex = '^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', message = "password has to be between 6-20 chars, a digit number, a uppercase and lowercase number, and a special character")])
    password = StringField("Password", validators = [InputRequired(), Length(min = 1, max = 20, message = "20 char limit")])
    # recaptcha = RecaptchaField(validators = [InputRequired()])
    submit = SubmitField(label = "Submit")

class loginform(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField(label = "Submit")

class settingsform(FlaskForm):
    pass

class taskfillform(FlaskForm):
    priority = SelectField("Indicate priority please", validators = [InputRequired()], choices = [(1), (2), (3)])
    task = StringField("Give a name to your task", validators = [InputRequired(), Length(max = 20, message = "20 char limit")])
    duedate = DateField("Indicate due date if any", validators = [Optional()], format = "%Y-%m-%d")
    details = TextAreaField("Elaborate task", validators = [Length(max = 250, message = "Longer than 250 chars")], description = "Max 260 chars.", name = "details")
    submit = SubmitField(label = "Submit")

class tasklistform(FlaskForm):
    complete_checkbox = BooleanField()
    delete_checkbox = BooleanField()
    submit = SubmitField(label = "Submit")

class complistform(FlaskForm):
    delete_checkbox = BooleanField()
    submit = SubmitField(label = "Submit")

class changepasswordform(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    old_password = StringField("Enter your old password", validators = [InputRequired()])
    new_password1 = StringField("Enter your new password", validators = [InputRequired(), Length(max = 20, message = "20 char limit")])
    new_password2 = StringField("Re-enter your new password", validators = [InputRequired(), Length(max = 20, message = "20 char limit")])
    submit = SubmitField(label = "Change password")