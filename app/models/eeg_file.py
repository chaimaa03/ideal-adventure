from datetime import datetime
from ..extensions import db

class EEGFile(db.Model):
    __tablename__ = 'eeg_files'

    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('patient_states.id', ondelete='CASCADE'), nullable=False, unique=True)
    eeg_folder_id = db.Column(db.Integer, db.ForeignKey('eeg_folders.id', ondelete='CASCADE'), nullable=True)

    report = db.relationship(
    'AnalysisReport',
    backref='eeg_file',
    cascade='all, delete-orphan',
    passive_deletes=True,
    uselist=False
    )


    diagnosis = db.Column(db.String(255), nullable=True)  # ML/DL diagnosis
    confidence_level = db.Column(db.Float, nullable=True)  # Average confidence level
    rhythm_analysis = db.Column(db.String(255), nullable=True)  # Rhythm analysis
    analyzed_at = db.Column(db.DateTime, nullable=True)  # Timestamp for when the report was generated
    
    def __repr__(self):
        return f"<EEGFile id={self.id} file='{self.file_name}' patient_id={self.patient_id}>"

