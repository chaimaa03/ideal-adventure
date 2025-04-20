from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:EEG_application@localhost/eeg_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One user can have many patients
    patients = db.relationship('Patient', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    states = db.relationship('PatientState', backref='patient', lazy=True, cascade='all, delete-orphan')

class PatientState(db.Model):
    __tablename__ = 'patient_states'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    conditions = db.Column(db.Text)
    sleep_patterns = db.Column(db.Text)
    stress_level = db.Column(db.String(20))
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    
    # Relationships:
    # One state can have many EEG files
    eeg_files = db.relationship('EEGFile', backref='state', lazy=True)
    # One state can have many analysis reports
    reports = db.relationship('AnalysisReport', backref='state', lazy=True)

class EEGFile(db.Model):
    __tablename__ = 'eeg_files'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    state_id = db.Column(db.Integer, db.ForeignKey('patient_states.id', ondelete='CASCADE'))
    
    # Relationship: One EEG file has one analysis report
    analysis = db.relationship('AnalysisReport', backref='eeg_file', uselist=False)

class AnalysisReport(db.Model):
    __tablename__ = 'analysis_reports'
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(100), nullable=False)
    confidence_level = db.Column(db.Float)
    rhythm_analysis = db.Column(db.Text)
    anomalies = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    state_id = db.Column(db.Integer, db.ForeignKey('patient_states.id'))
    eeg_id = db.Column(db.Integer, db.ForeignKey('eeg_files.id'))

# --- API ROUTES ---

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the EEG API"}), 200

@app.route('/tables')
def show_tables():
    #Render an HTML page displaying database tables.
    users = User.query.all()
    patients = Patient.query.all()
    states = PatientState.query.all()
    eeg_files = EEGFile.query.all()
    reports = AnalysisReport.query.all()
    
    return render_template('tables.html', 
                         users=users, 
                         patients=patients,
                         states=states,
                         eeg_files=eeg_files,
                         reports=reports)



@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "created_at": u.created_at} for u in users])


@app.route('/api/register', methods=['POST'])
def register():
    #Create a new user account
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/api/patients', methods=['POST'])
def create_patient():
    #Add a new patient record
    data = request.get_json()
    try:
        patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date(),
            sex=data['sex'],
            user_id=data['user_id']
        )
        db.session.add(patient)
        db.session.commit()
        return jsonify({"patient_id": patient.id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


    
#curl -X POST http://localhost:5000/api/patients \
#-H "Content-Type: application/json" \
#-d '{"first_name":"Emma","last_name":"Smith","birth_date":"1990-01-01","sex":"Female","user_id":1}'


@app.route('/api/patients/<int:patient_id>/states', methods=['POST'])
def add_state(patient_id):
    #Add a health state for a patient
    data = request.get_json()
    state = PatientState(
        weight=data.get('weight'),
        height=data.get('height'),
        conditions=data.get('conditions'),
        patient_id=patient_id
    )
    db.session.add(state)
    db.session.commit()
    return jsonify({"state_id": state.id}), 201

@app.route('/api/dashboard')
def get_dashboard():
    #Get dashboard statistics
    total_patients = Patient.query.count()
    recent_reports = AnalysisReport.query.order_by(AnalysisReport.analyzed_at.desc()).limit(5).all()
    
    return jsonify({
        "total_patients": total_patients,
        "recent_reports": [
            {"id": r.id, "diagnosis": r.diagnosis} 
            for r in recent_reports
        ]
    })

@app.route('/api/tables', methods=['GET'])
def get_tables():
     #Fetch all tables in the database
     result = db.session.execute("SHOW TABLES")
     tables = [row[0] for row in result]
     return jsonify({"tables": tables})

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/patients')
def show_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/states')
def show_states():
    states = PatientState.query.all()
    return render_template('states.html', states=states)

@app.route('/eegfiles')
def show_eegfiles():
    eeg_files = EEGFile.query.all()
    return render_template('eegfiles.html', eeg_files=eeg_files)

@app.route('/reports')
def show_reports():
    reports = AnalysisReport.query.all()
    return render_template('reports.html', reports=reports)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all database tables
    app.run(debug=True) 