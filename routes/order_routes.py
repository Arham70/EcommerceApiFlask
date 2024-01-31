from flask import Blueprint, jsonify, request
from models.order import Order
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


order_bp = Blueprint('order', __name__)

@order_bp.route('/order_history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()

    # Create a list to store order data
    order_history = []
    for order in orders:
        order_data = {
            'order_id': order.id,
            'total_price': order.total_price,
            'date_ordered': order.date_ordered,
            'products': [product.name for product in order.products]
        }
        order_history.append(order_data)

    return jsonify({'order_history': order_history})
