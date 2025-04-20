from flask import Blueprint, request, jsonify
from ..models.eeg_file import EEGFile
from ..models.patient_state import PatientState
from ..models.analysis_report import AnalysisReport
from ..models.run_cnn import run_cnn_model
from ..extensions import db

eeg_file_bp = Blueprint('eeg_file', __name__, url_prefix='/eeg-files')

# Create EEG file
def create_eeg_file():
    data = request.get_json()

    try:
        # Step 1: Create EEG file
        eeg_file = EEGFile(
            file_name=data['file_name'],
            file_path=data['file_path'],
            eeg_folder_id=data['eeg_folder_id']
        )
        db.session.add(eeg_file)
        db.session.flush()  # Get eeg_file.id

        # Step 2: Create patient state (neurological exam info)
        state = PatientState(
            status=data['state'],
            eeg_id=eeg_file.id
        )
        db.session.add(state)

        # Step 3: Run CNN model on EEG image (mocked for now)
        # You can replace this block with actual model code
        diagnosis, confidence, rhythm, anomalies = run_cnn_model(data['file_path'])

        # Step 4: Create the report automatically from model output
        report = AnalysisReport(
            diagnosis=diagnosis,
            confidence_level=confidence,
            rhythm_analysis=rhythm,
            anomalies=anomalies,
            eeg_id=eeg_file.id
        )
        db.session.add(report)

        db.session.commit()
        return jsonify({"eeg_file_id": eeg_file.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get all EEG files
@eeg_file_bp.route('/', methods=['GET'])
def get_all_eeg_files():
    eeg_files = EEGFile.query.all()
    result = [
        {
            "id": file.id,
            "file_name": file.file_name,
            "file_path": file.file_path,
            "created_at": file.created_at.isoformat(),
            "state_id": file.state_id,
            "eeg_folder_id": file.eeg_folder_id
        }
        for file in eeg_files
    ]
    return jsonify(result), 200

# Get single EEG file by ID
@eeg_file_bp.route('/<int:file_id>', methods=['GET'])
def get_eeg_file(file_id):
    file = EEGFile.query.get_or_404(file_id)
    return jsonify({
        "id": file.id,
        "file_name": file.file_name,
        "file_path": file.file_path,
        "created_at": file.created_at.isoformat(),
        "state_id": file.state_id,
        "eeg_folder_id": file.eeg_folder_id
    }), 200

# Delete EEG file
@eeg_file_bp.route('/<int:file_id>', methods=['DELETE'])
def delete_eeg_file(file_id):
    file = EEGFile.query.get_or_404(file_id)
    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "EEG file deleted"}), 200