from flask import Blueprint, request, jsonify,render_template,redirect,url_for
from ..models.eeg_folder import EEGFolder
from ..models.patient import Patient
from ..models.eeg_file import EEGFile
from ..extensions import db
from flask import flash

eeg_folder_bp = Blueprint('eeg_folder', __name__, url_prefix='/api/dashboard/folder')

@eeg_folder_bp.route('/patients/add_patient', methods=['GET', 'POST'])
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
            folder = EEGFolder.query.first()
            if not folder:
                folder = EEGFolder(
                    folder_name="Main Folder",
                    description="Single folder for all patients"
                )
                db.session.add(folder)
                db.session.flush()
            # Create a new patient
            new_patient = Patient(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                sex=sex,
                user_id=user_id,
                eeg_folder_id=folder.id
            )
            db.session.add(new_patient)
            db.session.commit()

            return redirect(url_for('eeg_folder.list_patients'))

        except Exception as e:
            db.session.rollback()
            print("Error while adding patient:", e)
            return f"An error occurred: {str(e)}", 500


@eeg_folder_bp.route('/', methods=['GET'])
def list_patients():
    folder = EEGFolder.query.first()  # Get the single folder
    if not folder:
        return "No folder found.", 404  # Return a 404 error if no folder exists

    patients = folder.patients  # Get the list of patients in the folder
    return render_template('folder_list.html', patients=patients)

# 3. Get all EEG files in for a patient
@eeg_folder_bp.route('/patients/<int:patient_id>/', methods=['GET'])
def get_patient_eeg_files(patient_id):
    # Fetch the patient by ID
    patient = Patient.query.get_or_404(patient_id)

    # Fetch all EEG files associated with the patient
    eeg_files = EEGFile.query.filter_by(patient_id=patient_id).all()

    # Render the template with patient info and EEG files
    return render_template(
        'patient_eeg_files.html',
        patient=patient,
        eeg_files=eeg_files
    )

@eeg_folder_bp.route('/patients/<int:patient_id>/delete', methods=['POST'])
def delete_patient(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        flash("Le patient a été supprimé avec succès.", "success")
        return redirect(url_for('eeg_folder.list_patients'))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "danger")
        return redirect(url_for('eeg_folder.list_patients'))


