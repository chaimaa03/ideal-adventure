
from ..models.patient_state import PatientState
from ..extensions import db
from flask import Blueprint, jsonify, request

patient_state_bp=Blueprint('patient_state', __name__, url_prefix='/api/patients')

@patient_state_bp.route('/<int:patient_id>/states', methods=['POST'])
def add_state(patient_id):
    #Add a health state for a patient
    data = request.get_json()
    state = PatientState(
        weight=data.get('weight'),
        height=data.get('height'),
        conditions=data.get('conditions'),
        patient_id=patient_id
    )
    db.session.add(state)
    db.session.commit()
    return jsonify({"state_id": state.id}), 201