from flask import Blueprint, render_template, url_for, session, redirect
from sqlalchemy import func, desc
from datetime import datetime
from ..extensions import db
from ..models import AnalysisReport, EEGFile, PatientState, Patient

dashboard_bp = Blueprint('dashboard', __name__,url_prefix='/api/dashboard')


@dashboard_bp.route('/', methods=['GET'])
def dashboard():

    #user_id = session.get('user_id')
    #if not user_id:
    #return redirect(url_for('auth.login'))

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