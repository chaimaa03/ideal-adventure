import pymysql
from flask import Flask, request, session
from .extensions import db, migrate


from .config import Config
from .routes import register_blueprints  # You can register multiple Blueprints here
from .models import ml_utils,users, patient , patient_state, eeg_file, eeg_folder, AnalysisReport
pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    

 
    
    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
   
 
    

    return app


