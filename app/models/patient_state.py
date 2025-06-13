from datetime import datetime
from ..extensions import db

class PatientState(db.Model):
    __tablename__ = 'patient_states'
    id = db.Column(db.Integer, primary_key=True)
    
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    
    suspicion_level = db.Column(db.String(50), nullable=False)  # "Faible", "Modéré", "Élevé"
    symptoms = db.Column(db.Text, nullable=False)  # Observed symptoms
    family_history = db.Column(db.String(10), nullable=False)  # "Oui" or "Non"
    cognitive_score = db.Column(db.String(255), nullable=True)  # Cognitive evaluation score or notes
    motor_observation = db.Column(db.String(50), nullable=True)  # "Normale" or "Anormale"
    speech_notes = db.Column(db.Text, nullable=True)  # Observations on speech
    social_behavior = db.Column(db.Text, nullable=True)  # Social behavior observations
    
   
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    # Optional relationship
    eeg_file = db.relationship('EEGFile', backref=db.backref('state', uselist=False, cascade='all, delete'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PatientState id={self.id} suspicion_level={self.suspicion_level}>"
    
