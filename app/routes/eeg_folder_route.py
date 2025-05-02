from flask import Blueprint, request, jsonify,render_template,redirect,url_for
from ..models.eeg_folder import EEGFolder
from ..models.patient import Patient
from ..models.eeg_file import EEGFile
from ..extensions import db

eeg_folder_bp = Blueprint('eeg_folder', __name__, url_prefix='/api/folders')

@eeg_folder_bp.route('/patient/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'GET':
        # Render the form for adding a patient
        return render_template('add_patient.html')
    elif request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            birth_date = request.form.get('birth_date')
            sex = request.form.get('sex')

            user_id = 1  # Replace with actual user ID logic if needed

            # Create a new patient
            new_patient = Patient(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                sex=sex,
                user_id=user_id
            )
            db.session.add(new_patient)
            db.session.flush()  # Flush to get the patient ID before committing

            # Create a folder for the new patient
            new_folder = EEGFolder(
                folder_name=f"{first_name} {last_name}'s Folder",
                description=f"Folder for patient {first_name} {last_name}",
                patient_id=new_patient.id
            )
            db.session.add(new_folder)

            # Commit both the patient and the folder
            db.session.commit()

            # Redirect to the list of folders
            return redirect(url_for('eeg_folder.list_folders'))
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}", 500


@eeg_folder_bp.route('/list', methods=['GET'])
def list_folders():
    patient_id = request.args.get('patient_id')
    if patient_id:
        folders = EEGFolder.query.filter_by(patient_id=patient_id).all()
    else:
        folders = EEGFolder.query.all()
    return render_template('folder_list.html', folders=folders)

# 3. Get all EEG files in a folder
@eeg_folder_bp.route('/<int:eeg_folder_id>/files', methods=['GET'])
def get_all_eeg_files(eeg_folder_id):
    eeg_files = EEGFile.query.filter_by(eeg_folder_id=eeg_folder_id).all()
    if not eeg_files:
        return jsonify({"message": "No EEG files found for this folder"}), 404
    return jsonify([
        {
            "id": file.id,
            "file_name": file.file_name,
            "file_path": file.file_path,
            "created_at": file.created_at.isoformat(),
            "state_id": file.state_id,
            "eeg_folder_id": file.eeg_folder_id
        } for file in eeg_files
    ])

@eeg_folder_bp.route('/<int:folder_id>', methods=['GET'])
def view_folder(folder_id):
    folder = EEGFolder.query.get_or_404(folder_id)
    patient = folder.patient  # Access the patient associated with the folder
    eeg_files = EEGFile.query.filter_by(eeg_folder_id=folder_id).all()
    return render_template(
        'folder_detail.html',
        folder=folder,
        patient=patient,
        eeg_files=eeg_files
    )
