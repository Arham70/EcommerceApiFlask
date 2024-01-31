from app import db

order_products = db.Table('order_products',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_price = db.Column(db.Float)
    date_ordered = db.Column(db.DateTime)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    products = db.relationship('Product', secondary=order_products, lazy='subquery',
                               backref=db.backref('orders', lazy=True))
