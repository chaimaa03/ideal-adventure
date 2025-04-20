from flask import Blueprint, request, jsonify
from ..models.analysis_report import AnalysisReport
from ..extensions import db

analysis_report_bp = Blueprint('analysis_report', __name__, url_prefix='/analysis-reports')

# POST: Create a new analysis report
@analysis_report_bp.route('/', methods=['POST'])
def create_analysis_report():
    data = request.get_json()

    try:
        report = AnalysisReport(
            diagnosis=data['diagnosis'],
            confidence_level=data.get('confidence_level'),
            rhythm_analysis=data.get('rhythm_analysis'),
            anomalies=data.get('anomalies'),
            state_id=data['state_id'],
            eeg_id=data['eeg_id']
        )
        db.session.add(report)
        db.session.commit()

        return jsonify({"report_id": report.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# GET: List all analysis reports
@analysis_report_bp.route('/', methods=['GET'])
def get_analysis_reports():
    reports = AnalysisReport.query.all()
    return jsonify([
        {
            "id": r.id,
            "diagnosis": r.diagnosis,
            "confidence_level": r.confidence_level,
            "rhythm_analysis": r.rhythm_analysis,
            "anomalies": r.anomalies,
            "analyzed_at": r.analyzed_at.isoformat(),
            "state_id": r.state_id,
            "eeg_id": r.eeg_id
        } for r in reports
    ])