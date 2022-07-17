from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, RadioField


class LoginForm(FlaskForm):
    # Sử dụng render_kw để hiện placehoder
    username = StringField("Username", render_kw={"placeholder": "Username"})
    password = PasswordField("Password", render_kw={"placeholder": "Password"})
    email = EmailField("Email", render_kw={"placeholder": "Email"})
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    # Sử dụng render_kw để hiện placehoder
    username = StringField("Username", render_kw={"placeholder": "Username"})
    password = PasswordField("Password", render_kw={"placeholder": "Password"})
    email = EmailField("Email", render_kw={"placeholder": "Email"})
    submit = SubmitField("Sign up")


class OccupationForm(FlaskForm):
    other = StringField("Other")
    occupation = RadioField("Occupation", choices=[("student", "Student"), ("teacher", "Teacher"), ("other", "Other")])
    submit = SubmitField("Submit")
