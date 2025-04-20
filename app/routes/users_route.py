from flask import Blueprint, jsonify, request, render_template, abort
from ..models.users import User
from ..extensions import db

user_bp = Blueprint('user',__name__, url_prefix='/api/users')

@user_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "created_at": u.created_at} for u in users])

@user_bp.route('/view', methods=['GET'])
def view_users():
    users = User.query.all()
    return render_template('users.html', users=users)