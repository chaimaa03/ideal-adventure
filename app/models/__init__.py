from flask_sqlalchemy import SQLAlchemy
from .users import User
from .patient import Patient
from .patient_state import PatientState
from .eeg_file import EEGFile
from .eeg_folder import EEGFolder
from .AnalysisReport import AnalysisReport



db = SQLAlchemy()
