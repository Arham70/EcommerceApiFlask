from flask import Blueprint, jsonify, request
from models.product import Product
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from config.database import db

product_bp = Blueprint('product', __name__)


@product_bp.route('/products', methods=['GET'])
@login_required
def get_all_products():
    products = Product.query.all()
    output = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category_id': product.category_id
        }
        output.append(product_data)
    return jsonify({'products': output})


@product_bp.route('/products/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'category_id': product.category_id
    }
    return jsonify(product_data)


@product_bp.route('/products', methods=['POST'])
@login_required
def add_product():
    data = request.json
    new_product = Product(name=data['name'], description=data['description'], price=data['price'], category_id=data['category_id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'})


@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})
