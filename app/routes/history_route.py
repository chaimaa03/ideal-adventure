from flask import Blueprint, jsonify, request
from ..models.history import History
from ..extensions import db

history_bp = Blueprint('history', __name__, url_prefix='/api/history')

@history_bp.route('/', methods=['GET'])
def get_history():
    history = History.query.order_by(History.viewed_at.desc()).all()
    return jsonify([{"id": h.id, "folder": h.folder, "file": h.file, "analysis": h.analysis} for h in history])

@history_bp.route('/', methods=['POST'])
def add_history():
    data = request.get_json()
    history = History(folder=data['folder'], file=data['file'], analysis=data['analysis'])
    db.session.add(history)
    db.session.commit()
    return jsonify({"id": history.id}), 201