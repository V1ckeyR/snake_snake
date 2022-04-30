from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):cd
        return f'<Category { self.name }>'
