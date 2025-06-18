from flask import Blueprint, request, redirect, url_for, render_template, flash
import joblib 
import tensorflow as tf
import mne
import numpy as np
from werkzeug.utils import secure_filename
from ..models.eeg_file import EEGFile
from ..models.eeg_folder import EEGFolder
from ..models.patient_state import PatientState
from ..models.patient import Patient
from ..models.AnalysisReport import AnalysisReport
from ..extensions import db
from app.models.ml_utils import extract_features_from_edf
from app.models.dl_utils import preprocess_edf_for_dl, dl_model
import os
from datetime import datetime

eeg_file_bp = Blueprint('eegfile', __name__, url_prefix='/api/dashboard/folder/patients')

UPLOAD_FOLDER = 'app/static/uploads/eeg/'
ALLOWED_EXTENSIONS = {'edf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@eeg_file_bp.route('<int:patient_id>/eegfile/add_eegfile', methods=['POST'])
def create_eegfile(patient_id):
# Get form data
    try:
        weight = request.form.get('weight')
        height = request.form.get('height')
        suspicion_level = request.form.get('suspicion_level')
        symptoms = request.form.get('symptoms')
        family_history = request.form.get('family_history')
        cognitive_score = request.form.get('cognitive_score')
        motor_observation = request.form.get('motor_observation')
        speech_notes = request.form.get('speech_notes')
        social_behavior = request.form.get('social_behavior')
        eeg_file = request.files.get('eeg_file')

        if not eeg_file or not allowed_file(eeg_file.filename):
            flash("Format EEG non valide.", 'danger')
            return redirect(request.referrer)

        filename = secure_filename(eeg_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        eeg_file.save(file_path)

        try:
            # 1. Create PatientState
            state = PatientState(
                 weight=weight,
                height=height,
                suspicion_level=suspicion_level,
                symptoms=symptoms,
                family_history=family_history,
                cognitive_score=cognitive_score,
                motor_observation=motor_observation,
                speech_notes=speech_notes,
                social_behavior=social_behavior,
                patient_id=patient_id
            )
            db.session.add(state)
            db.session.flush()

            # 2. Create EEGFile and link state
            eegfile = EEGFile(
                file_name=filename,
                file_path=file_path,
                patient_id=patient_id,
                state_id=state.id
            )
            db.session.add(eegfile)
            db.session.flush()
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", 'danger')  # Flash error in template
            print("Exception while creating EEG file:", e)  # Log error in console
            patient = Patient.query.get(patient_id)  # Reload context
            return render_template('add_state.html', patient=patient)

        # Update state with EEGFile ID (bidirectional)
        state.eeg_id = eegfile.id

        def predict_with_ml(file_path):
            ml_model = joblib.load('app/models/logistic_pipe_model.pkl')
            features = extract_features_from_edf(file_path)

            prediction = ml_model.predict(features)[0]
            prob = ml_model.predict_proba(features)[0].max()

            diagnosis = "Schizophrène" if prediction == 1 else "Sain"

            return {
                "diagnosis": diagnosis,
                "confidence": round(prob * 100, 2)  # return as percentage
            }
        def predict_with_dl(file_path):
            signal = preprocess_edf_for_dl(file_path)
            prediction = dl_model.predict(signal)[0]  # shape (n_classes,) or (1,)
    
        # Convert prediction to label
            predicted_class = np.argmax(prediction) if len(prediction) > 1 else int(prediction > 0.5)
            confidence = float(np.max(prediction)) if len(prediction) > 1 else float(prediction[0])

            return {
                "diagnosis": "Schizophrène" if predicted_class == 1 else "Sain",
                "confidence": round(confidence * 100, 2),
                "rhythm_analysis": "Normal" if predicted_class == 0 else "Anormal"
          }

        # 3. Run ML & DL models
        ml_result = predict_with_ml(file_path)
        dl_result = predict_with_dl(file_path)

        # Retrieve patient info for report context
        patient = Patient.query.get_or_404(patient_id)
        age = (datetime.utcnow().date() - patient.birth_date).days // 365

        # 4. Generate report
        report = AnalysisReport(
            diagnosis=f"ML: {ml_result['diagnosis']} / DL: {dl_result['diagnosis']}",
            confidence_level=(ml_result['confidence'] + dl_result['confidence']) / 2,
            rhythm_analysis=dl_result['rhythm_analysis'],
            patient_age=age,
            patient_sex=patient.sex,
            eeg_id=eegfile.id,
            analyzed_at=datetime.utcnow()
        )
        db.session.add(report)
        db.session.commit()

        return redirect(url_for('eegfile.view_eegfile',patient_id=patient_id, eegfile_id=eegfile.id))
    except Exception as e:
        print("Error during EEG file creation:", e)
        return f"An error occurred: {str(e)}", 500
    

@eeg_file_bp.route('/<int:patient_id>/eegfile/<int:eegfile_id>')
def view_eegfile(patient_id, eegfile_id):
    eegfile = EEGFile.query.get_or_404(eegfile_id)
    if eegfile.patient_id != patient_id:
        flash("EEG file does not belong to the specified patient.", 'danger')
        return redirect(url_for('dashboard_bp.dashboard'))
    state = eegfile.state
    report = AnalysisReport.query.filter_by(eeg_id=eegfile.id).first()
    patient = eegfile.patient

    return render_template('eeg_file_detail.html', eegfile=eegfile, state=state, report=report, patient=patient)

@eeg_file_bp.route('/<int:patient_id>/eegfile/add', methods=['GET'])
def show_eegfile_form(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('add_state.html', patient=patient)
