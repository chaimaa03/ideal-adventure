from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from ..models import User
from ..extensions import db, mail
from flask_mail import Message
from ..forms.auth_forms import RegisterForm,LoginForm,ResetPasswordRequestForm,ResetPasswordForm
from datetime import datetime
auth_bp = Blueprint('auth', __name__,url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.')
            return redirect(url_for('auth.register'))

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Un compte avec cet email existe déjà.')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.confirmation'))

    return render_template('auth/register.html',form=form)

# -------------------- Confirmation après inscription --------------------
@auth_bp.route('/confirmation')
def confirmation():
    return render_template('auth/confirmation.html')

# -------------------- Connexion --------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Email ou mot de passe incorrect.")
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        return redirect(url_for('dashboard.dashboard'))

    return render_template('auth/login.html',form=form)

# -------------------- Réinitialisation du mot de passe (demande) --------------------
@auth_bp.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    form=ResetPasswordRequestForm()
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = generate_reset_token(user.email)
            reset_link = url_for('auth.reset_password', token=token, _external=True)

            # Envoyer l’email
            msg = Message("Réinitialisation du mot de passe", recipients=[user.email])
            msg.body = f"Voici votre lien pour réinitialiser le mot de passe : {reset_link}\nCe lien expire dans 30 minutes."
            mail.send(msg)

            flash("Un email de réinitialisation a été envoyé.")
            return redirect(url_for('auth.login'))
        else:
            flash("Aucun compte trouvé avec cet email.")
            return redirect(url_for('auth.reset_request'))

    return render_template('auth/reset_request.html',form=form)

# -------------------- Réinitialisation du mot de passe (via lien) --------------------
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form=ResetPasswordForm()
    try:
        email = verify_reset_token(token)
    except (SignatureExpired, BadSignature):
        flash("Lien invalide ou expiré.")
        return redirect(url_for('auth.reset_request'))

    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm = request.form['confirm_password']

        if new_password != confirm:
            flash("Les mots de passe ne correspondent pas.")
            return redirect(url_for('auth.reset_password', token=token))

        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()

        flash("Mot de passe réinitialisé avec succès.")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html',form=form)

def generate_reset_token(email, expires_sec=1800):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='reset-password')

def verify_reset_token(token, expires_sec=1800):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.loads(token, salt='reset-password', max_age=expires_sec)


