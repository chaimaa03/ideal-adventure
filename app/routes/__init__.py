from flask import Blueprint

# Import your blueprints
from .auth_route import auth_bp
from .eeg_folder_route import eeg_folder_bp
from .dashboard_route import dashboard_bp
from .eeg_file_route import eeg_file_bp
from .history_route import history_bp
from .base import base_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(eeg_folder_bp, url_prefix='/api/dashboard/folder')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(eeg_file_bp, url_prefix='/api/dashboard/folder/patients')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(base_bp, url_prefix='/')
