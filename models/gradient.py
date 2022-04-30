from app import db


class Gradient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, default='linear-gradient', nullable=False)
    direction = db.Column(db.String, nullable=False)
    colors = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Gradient { self.type }({ self.direction }, { self.colors })>'
