from datetime import datetime

from app import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.ENUM('pending', 'processing', 'completed', 'cancelled'))
    total_price = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Order #{ self.id }>'
