from flask import Blueprint, render_template, url_for, session, redirect,request,flash
from sqlalchemy import func, desc
from datetime import datetime
from ..models.users import User
from ..extensions import db
from flask import session, request

from ..models import AnalysisReport, EEGFile, PatientState, Patient

dashboard_bp = Blueprint('dashboard', __name__,url_prefix='/api/dashboard')


@dashboard_bp.route('/', methods=['GET'])
def dashboard():

    user_id = session.get('user_id')
    if not user_id:
      return redirect(url_for('auth.login'))

    # Nombre total de patients
    total_patients = db.session.query(func.count(Patient.id)).scalar()

    # Nombre total d'analyses effectuées
    total_analyses = db.session.query(func.count(EEGFile.id)).scalar()

    # Récupération du diagnostic le plus fréquent
    most_common = db.session.query(
        AnalysisReport.diagnosis,
        func.count(AnalysisReport.id).label("count")
    ).group_by(AnalysisReport.diagnosis).order_by(desc("count")).first()

    if most_common and total_analyses:
        most_common_diagnosis = most_common.diagnosis
        accuracy_percentage = round((most_common.count / total_analyses) * 100, 2)
    else:
        most_common_diagnosis = "Aucun"
        accuracy_percentage = 0

    # Récupération de la dernière analyse
    last_file = db.session.query(EEGFile).order_by(EEGFile.id.desc()).first()

    last_analysis = None
    if last_file and last_file.patient:
        try:
            # Recherche de l'état et du patient associé
            patient_state = PatientState.query.get(last_file.state_id)
            patient_name = "Inconnu"
            patient_age = "Inconnu"
            patient_gender = "Inconnu"

            if patient_state:
                patient = Patient.query.get(patient_state.patient_id)
                if patient:
                    patient_name = f"{patient.first_name} {patient.last_name}"
                    patient_gender = patient.sex
                    patient_age = (datetime.utcnow().date() - patient.birth_date).days // 365
            
            last_analysis = {
                "patient_name": patient_name,
                "date": last_file.patient.created_at.strftime("%Y-%m-%d %H:%M"),
                "age": patient_age,
                "sex": patient_gender
            }
        except Exception as e:
            print("Erreur lors de la récupération de la dernière analyse :", e)

    # Affichage du template avec les données
    return render_template(
        "dashboard/dashboard.html",
        last_analysis=last_analysis,
        total_analyses=total_analyses,
        total_patients=total_patients,
        most_common_diagnosis=most_common_diagnosis,
        accuracy_percentage=accuracy_percentage
    )

@dashboard_bp.route('/profile')
def profile():
    user_id = session.get('user_id')

    # Récupère l'objet utilisateur en base
    user = User.query.get(user_id)
    if not user:
        return "Utilisateur introuvable", 404

    # Calcul de l'ancienneté du compte en jours
    account_age = (datetime.utcnow() - user.created_at).days

    return render_template('dashboard/profile.html', user=user, account_age_days=account_age)

@dashboard_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)  # ✅ correction ici
    if not user:
        flash("Utilisateur introuvable.")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not user.check_password(current_password):
            flash("Ancien mot de passe incorrect.")
            return redirect(url_for('dashboard.settings'))

        if new_password != confirm_password:
            flash("Les nouveaux mots de passe ne correspondent pas.")
            return redirect(url_for('dashboard.settings'))

        if len(new_password) < 8:
            flash("Le mot de passe doit contenir au moins 8 caractères.")
            return redirect(url_for('dashboard.settings'))

        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()

        flash("Mot de passe mis à jour avec succès.")
        return redirect(url_for('dashboard.settings'))

    return render_template('dashboard/settings.html', user=user) 



