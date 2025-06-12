import pymysql
from flask import Flask
from .extensions import db, migrate
from .config import Config
from .routes import register_blueprints  # You can register multiple Blueprints here
from .models import ml_utils,users, patient , patient_state, eeg_file, eeg_folder, AnalysisReport, history
pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register all Blueprints
    register_blueprints(app)

    return app