import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e97efe91a4fefa4d8ae0ae78bdd5a3be01b13850537a6db8e4207bf88a82a781'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_user:EEG_application@localhost/eeg_system'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://flask_user:EEG_application@localhost/eeg_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)