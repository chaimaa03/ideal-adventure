from flask import Blueprint, request, jsonify
from ..models.users import User
from ..extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'])
    user.password_hash(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


