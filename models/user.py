from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub = db.Column(db.String(255), unique=True, nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=True)

    @staticmethod
    def add(sub, nickname, picture):
        db.session.add(User(sub=sub, nickname=nickname, picture=picture))
        db.session.commit()

    def __repr__(self):
        return f'<User { self.sub }>'
