from datetime import datetime
from ..extensions import db

class PatientState(db.Model):
    __tablename__ = 'patient_states'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    conditions = db.Column(db.Text) #we need patient's file 
    sleep_patterns = db.Column(db.Text)
    stress_level = db.Column(db.String(20))
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    eeg_id = db.Column(db.Integer, db.ForeignKey('eeg_files.id'), nullable=False)
    
    # Relationships:
    # One state can have many EEG files
    eeg_files = db.relationship('EEGFile', foreign_keys=[eeg_id], backref='state', lazy=True)
    # One state can have many analysis reports
    reports = db.relationship('AnalysisReport', backref='state', lazy=True)
