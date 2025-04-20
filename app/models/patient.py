from datetime import datetime
from ..extensions import db

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship: One patient can have many states
    folder = db.relationship('EEGFolder', uselist=False, backref='patient', cascade='all, delete-orphan')
    states = db.relationship('PatientState', backref='patient', lazy=True, cascade='all, delete-orphan')
