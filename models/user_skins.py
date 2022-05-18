from app import db


class UserSkins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skin = db.Column(db.Integer, db.ForeignKey('skin.id'), nullable=False)

    def __repr__(self):
        return f'<User #{ self.user } has skin { self.skin }>'
