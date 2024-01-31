from flask import Blueprint, jsonify, request
from models.user import User
from config.database import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@login_required
def get_all_users():
    users = User.query.all()
    output = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify({'users': output})

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {'id': user.id, 'username': user.username}
    return jsonify(user_data)


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

