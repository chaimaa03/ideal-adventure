from flask import Blueprint, render_template, request, jsonify, redirect,url_for
from datetime import datetime
from ..models.patient import Patient
from ..models.eeg_file import EEGFile
from ..models.eeg_folder import EEGFolder
from ..extensions import db



patient_bp=Blueprint('patient', __name__, url_prefix='/api/patients')



        
@patient_bp.route('/', methods=['GET'])
def view_patients():
    print("view_patients route called")
    patients = Patient.query.all()
    return render_template('patient.html', patients=patients)

@patient_bp.route('/<int:patient_id>', methods=['GET'])
def view_patient( patient_id):
    patient = Patient.query.get_or_404(patient_id)
    eeg_files = EEGFile.query.filter_by(patient_id=patient_id).all()
    return render_template('patient_detail.html', patient=patient, eeg_files=eeg_files)

@patient_bp.route('/list', methods=['GET'])
def list_patients():
    print("list_patients route called")
    patients = Patient.query.all()
    return jsonify([
        {
            "id": patient.id,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "birth_date": patient.birth_date.isoformat(),
            "sex": patient.sex,
            "eeg_folder": patient.eeg_folder.folder_name if patient.eeg_folder else None
        } for patient in patients
    ])