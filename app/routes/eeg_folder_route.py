from flask import Blueprint, request, jsonify
from ..models.eeg_folder import EEGFolder
from ..models.eeg_file import EEGFile
from ..extensions import db

eeg_folder_bp = Blueprint('eeg_folder', __name__, url_prefix='/api/eeg-folders')

# 1. Create a folder
@eeg_folder_bp.route('', methods=['POST'])
def create_folder():
    data = request.get_json()
    folder = EEGFolder(
        name=data['name'],
        patient_id=data['patient_id']
    )
    db.session.add(folder)
    db.session.commit()
    return jsonify({"folder_id": folder.id, "message": "Folder created"}), 201

# 2. List folders for a patient
@eeg_folder_bp.route('/patient/<int:patient_id>', methods=['GET'])
def list_folders(patient_id):
    folders = EEGFolder.query.filter_by(patient_id=patient_id).all()
    return jsonify([
        {"id": f.id, "name": f.name, "created_at": f.created_at.isoformat()}
        for f in folders
    ])

# 3. Get all EEG files in a folder
@eeg_folder_bp.route('/<int:folder_id>/files', methods=['GET'])
def get_files_in_folder(folder_id):
    files = EEGFile.query.filter_by(folder_id=folder_id).all()
    return jsonify([
        {"id": f.id, "file_name": f.file_name, "created_at": f.created_at.isoformat()}
        for f in files
    ])
