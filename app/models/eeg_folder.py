from datetime import datetime
from ..extensions import db

class EEGFolder(db.Model):
    __tablename__ = 'eeg_folders'

    id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    # Relationship: One folder has many EEG files
    eeg_files = db.relationship('EEGFile', backref='folder', lazy=True, cascade='all, delete-orphan')
    patients = db.relationship('Patient', backref='eeg_folder', lazy=True,cascade="all, delete-orphan")

