from flask import Blueprint, jsonify, request
from models.category import Category
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config.database import db

category_bp = Blueprint('category', __name__)


@category_bp.route('/categories', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    output = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify({'categories': output})

@category_bp.route('/categories', methods=['POST'])
@login_required
def add_category():
    data = request.json
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'})

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully'})


