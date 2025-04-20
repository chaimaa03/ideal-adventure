from datetime import datetime
from ..extensions import db

class EEGFile(db.Model):
    __tablename__ = 'eeg_files'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    state_id = db.Column(db.Integer, db.ForeignKey('patient_states.id', ondelete='CASCADE'))
    
    # Relationship: One EEG file has one analysis report
    analysis = db.relationship('AnalysisReport', backref='eeg_file', uselist=False, cascade='all, delete-orphan')
    eeg_folder_id = db.Column(db.Integer, db.ForeignKey('eeg_folders.id', ondelete='CASCADE'), nullable=True)
    state = db.relationship('PatientState', foreign_keys=[state_id], uselist=False, backref='eeg_file', cascade='all, delete-orphan')


