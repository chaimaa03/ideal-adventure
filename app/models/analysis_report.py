from datetime import datetime
from ..extensions import db

class AnalysisReport(db.Model):
    __tablename__ = 'analysis_reports'
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(100), nullable=False)
    confidence_level = db.Column(db.Float)
    rhythm_analysis = db.Column(db.Text)
    anomalies = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    state_id = db.Column(db.Integer, db.ForeignKey('patient_states.id'))
    eeg_id = db.Column(db.Integer, db.ForeignKey('eeg_files.id'), nullable=False)
