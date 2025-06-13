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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Relationship: One patient can have many states
    
    eeg_folder_id = db.Column(db.Integer, db.ForeignKey('eeg_folders.id', ondelete='CASCADE'))
    states = db.relationship(
    'PatientState',
    backref='patient',
    cascade='all, delete-orphan',
    passive_deletes=True
   )
    eeg_files = db.relationship('EEGFile', backref='patient', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Patient id={self.id} name={self.first_name} {self.last_name}>"
    