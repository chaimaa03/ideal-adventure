from flask import Blueprint, request, jsonify
from ..models.patient import Patient
from ..models.analysis_report import AnalysisReport
from ..extensions import db

dashboard_bp = Blueprint('dashboard', __name__,url_prefix='/api/dashboard')


@dashboard_bp.route('', methods=['GET'])
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
