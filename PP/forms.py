from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


# Done
class LoginForm(FlaskForm):
    generated_id = StringField('Patient ID', validators=[])
    password = PasswordField('Password', validators=[])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


# Done
class RegisterForm(FlaskForm):
    name = StringField('Patient Full Name', validators=[DataRequired("Please enter full name")])
    email = StringField('Patient Email Address', validators=[Email('Please enter a valid email')])
    phone = IntegerField('Phone Number', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = StringField('Gender', validators=[DataRequired()])
    image_file = FileField('Profile Picture', default='Default.jpg', validators=[DataRequired("Your profile Picture is Needed."), FileAllowed(['jpg', 'png'])])
    doc_name = StringField('Your doctors name', validators=[DataRequired()])
    doc_mail = StringField('Your doctors Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired("Must be equal to password"), EqualTo('password')])
    submit = SubmitField('Register')


# Done
class UpdateDetailsForm(FlaskForm):
    name = StringField('Patient Full Name', validators=[DataRequired('Please enter your name')])
    email = StringField('Patient Email Address', validators=[DataRequired('Enter Email Address'), Email()])
    phone = IntegerField('Phone Number', validators=[DataRequired('Enter phone number')])
    age = IntegerField('Age', validators=[DataRequired('Enter your age')])
    sex = StringField('Gender', validators=[DataRequired('Enter gender here')])
    image_file = FileField('Profile Picture', validators=[DataRequired('Must add a profile image')])
    password = PasswordField('Password', validators=[DataRequired('Enter password here')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired('Enter confirmation password'), EqualTo('password')])
    submit = SubmitField('Update')


class NewAppointmentForm(FlaskForm):
    # name = StringField('Patient Full Name', validators=[DataRequired("Please enter full name")])
    email = StringField('Patient Email Address', validators=[DataRequired('Please enter a valid email')])
    image_file = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password', validators=[DataRequired("This field is required")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired("Must be equal to password"), EqualTo('password')])
    submit = SubmitField('Create appointment')


#Done
class MessageForm(FlaskForm):
    subject = StringField('Subject:', validators=[DataRequired('Type in the subject of your message'),
                                                  Length(min=10, max=30)])
    msg = TextAreaField('Type message here:', validators=[DataRequired('A message has to be here to send')])
    submit = SubmitField('Send Message')

