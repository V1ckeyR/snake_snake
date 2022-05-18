from app import db


class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    skin = db.Column(db.Integer, db.ForeignKey('skin.id'), nullable=False)

    order_relationship = db.relationship('Order', backref=db.backref('order_details', lazy=True))

    def __repr__(self):
        return f'<Order #{ self.order } includes skin { self.skin }>'
