from app.extensions import db
from datetime import datetime

class AnalysisReport(db.Model):
    __tablename__ = 'analysis_reports'
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(255), nullable=False)  # ML/DL diagnosis
    confidence_level = db.Column(db.Float, nullable=False)  # Average confidence level
    rhythm_analysis = db.Column(db.String(255), nullable=True)  # Rhythm analysis
    patient_age = db.Column(db.Integer, nullable=False)  # Patient's age at the time of analysis
    patient_sex = db.Column(db.String(10), nullable=False)  # Patient's sex
    eeg_id = db.Column(db.Integer, db.ForeignKey('eeg_files.id', ondelete='CASCADE'), nullable=False)  # Link to EEGFile
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for when the report was generated

    # Relationships
    eeg_file = db.relationship('EEGFile', backref='analysis_reports', lazy=True,cascade="all, delete-orphan")