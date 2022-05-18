from app import db


class Skin(db.Model):
    """
    Params for category 'color': 'hex'
    Params for category 'gradient': 'direction', 'colors'
    """

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    params = db.Column(db.JSON, nullable=False)

    @staticmethod
    def add(category, params):
        db.session.add(Skin(category=category, params=params))
        db.session.commit()

    def __repr__(self):
        return f'<Skin { self.category } with params { self.params }>'
