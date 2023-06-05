import bcrypt

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    # sub = db.Column(db.String(255), unique=True, nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False, default='#FFFFFF')
    picture = db.Column(db.LargeBinary, nullable=True)
    # time last login - to remove not required accounts


    @staticmethod
    def add(sub, nickname, picture):
        db.session.add(User(sub=sub, nickname=nickname, picture=picture))
        db.session.commit()
    def set_password(self, password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = password_hash.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User { self.sub }>'
