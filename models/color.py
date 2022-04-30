from app import db


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hex = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Color { self.hex }>'
