from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired,Length, Email, EqualTo, ValidationError
from application.models import *

class RegistrationForm(FlaskForm):
    username = StringField("Username",validators = [DataRequired(),Length(min=2,max=20)])
    email = StringField("Email",validators = [DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField("Email",validators = [DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Login")

class CreateVenueForm(FlaskForm):
    venue_name = StringField("Venue Name",validators=[DataRequired()])
    venue_address = StringField("Venue Address")
    venue_capacity = IntegerField("Venue Capacity")
    submit = SubmitField("Create Venue")

class UpdateVenueForm(FlaskForm):
    venue_name = StringField("Venue Name",validators=[DataRequired()])
    venue_address = StringField("Venue Address")
    venue_capacity = IntegerField("Venue Capacity")
    submit = SubmitField("Update Venue")

class CreateShowForm(FlaskForm):
    venue_id = IntegerField("Venue Id",validators=[DataRequired()])
    show_name = StringField("Venue Name",validators=[DataRequired()])
    show_rating = IntegerField("Show rating")
    show_ticket_price = IntegerField("Show ticket price")
    submit = SubmitField("Create Show")

class UpdateShowForm(FlaskForm):
    venue_id = IntegerField("Venue Id",validators=[DataRequired()])
    show_name = StringField("Venue Name",validators=[DataRequired()])
    show_rating = IntegerField("Show rating")
    show_ticket_price = IntegerField("Show ticket price")
    submit = SubmitField("Update Show")

class BookingForm(FlaskForm):
    show_id = IntegerField("Show Id",validators=[DataRequired()])
    quantity = IntegerField("Quantity",validators=[DataRequired()])
    submit = SubmitField("Book Show")