from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from models.cart_items import CartItem
from models.product import Product
from models.order import Order
from datetime import datetime
from config.database import db
from extensions.stripe import stripe_keys

cart_item_bp = Blueprint('cart_item', __name__)

@cart_item_bp.route('/cartitems', methods=['GET'])
def get_cart_items():
    # Retrieve cart items for the currently logged-in user
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    output = [{'id': item.id, 'user_id': item.user_id, 'product_id': item.product_id, 'quantity': item.quantity} for item in cart_items]
    return jsonify({'cart_items': output})

@cart_item_bp.route('/cartitems', methods=['POST'])
@login_required
def add_cart_item():
    data = request.json
    # Create a new cart item with the user_id set to the currently logged-in user
    new_cart_item = CartItem(user_id=current_user.id, product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_cart_item)
    db.session.commit()
    return jsonify({'message': 'Cart item added successfully'})

@cart_item_bp.route('/cartitems/<int:cart_item_id>', methods=['PUT'])
@login_required
def update_cart_item(cart_item_id):
    data = request.json
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access to update cart item'}), 403
    cart_item.product_id = data['product_id']
    cart_item.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Cart item updated successfully'})

@cart_item_bp.route('/cartitems/<int:cart_item_id>', methods=['DELETE'])
@login_required
def delete_cart_item(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access to delete cart item'}), 403
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Cart item deleted successfully'})


@cart_item_bp.route('/index')
@login_required
def index():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('index.html', key=stripe_keys['publishable_key'], total_price=total_price)

@cart_item_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    new_order = Order(user_id=current_user.id, total_price=total_price, date_ordered=datetime.utcnow())
    db.session.add(new_order)
    db.session.commit()

    for cart_item in cart_items:
        new_order.products.append(cart_item.product)

    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return render_template('checkout.html', total_price=total_price)