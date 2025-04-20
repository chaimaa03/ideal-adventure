from flask import Blueprint

# Import your blueprints
from .auth_route import auth_bp
from .users_route import user_bp
from .patient_route import patient_bp
from .eeg_folder_route import eeg_folder_bp
from .dashboard_route import dashboard_bp
from .eeg_file_route import eeg_file_bp
from .analysis_report_route import analysis_report_bp
from .patient_state_route import patient_state_bp
from .history_route import history_bp
from .base import base_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(patient_bp, url_prefix='/api/patients')
    app.register_blueprint(eeg_folder_bp, url_prefix='/api/folders')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(eeg_file_bp, url_prefix='/api/files')
    app.register_blueprint(analysis_report_bp, url_prefix='/api/reports')
    app.register_blueprint(patient_state_bp, url_prefix='/api/states')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(base_bp, url_prefix='/')
