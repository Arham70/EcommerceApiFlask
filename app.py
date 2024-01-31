from flask import Flask
from config.database import db
from extensions.stripe import stripe_keys
from routes.auth import *
from routes.product_routes import *
from routes.category_routes import *
from routes.cart_items_routes import *
from routes.order_routes import *
from routes.user_routes import *
from flask_login import LoginManager
from models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '*S@LIO%S400YJKFVZ_@0&WUC'  # Change this to a random string

# Initialize database
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register blueprint routes
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(cart_item_bp)
app.register_blueprint(order_bp)
app.register_blueprint(user_bp)

# Create all database tables within the application context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
