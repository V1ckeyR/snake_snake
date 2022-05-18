from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    @staticmethod
    def add(name, cost):
        db.session.add(Category(name=name, cost=cost))
        db.session.commit()

    def __repr__(self):
        return f'<Category { self.name }>'
