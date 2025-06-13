from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="L'email est requis."),
        Email(message="Format d'email invalide.")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message="Le mot de passe est requis.")
    ])
    submit = SubmitField('Connexion')


class RegisterForm(FlaskForm):
    username = StringField('Nom d’utilisateur', validators=[
        DataRequired(message="Le nom d’utilisateur est requis."),
        Length(min=3, max=20, message="Le nom doit avoir entre 3 et 20 caractères.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="L'email est requis."),
        Email(message="Format d'email invalide.")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(message="Le mot de passe est requis."),
        Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères.")
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(message="Confirmation requise."),
        EqualTo('password', message="Les mots de passe ne correspondent pas.")
    ])
    submit = SubmitField('S’inscrire')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')