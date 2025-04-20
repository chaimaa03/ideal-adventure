from flask import Blueprint, request, jsonify
from datetime import datetime
from ..models.patient import Patient
from ..models.eeg_file import EEGFile
from ..extensions import db

patient_bp=Blueprint('patient', __name__, url_prefix='/api/patients')

@patient_bp.route('', methods=['POST'])
def create_patient():
    #Add a new patient record
    data = request.get_json()
    try:
        patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date(),
            sex=data['sex'],
            user_id=data['user_id']
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({"patient_id": patient.id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
