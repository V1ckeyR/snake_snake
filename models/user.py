from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String, unique=True, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<User { self.nickname }>'
