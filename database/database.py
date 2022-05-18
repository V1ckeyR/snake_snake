import os
import json

from app import db
from models import *


FIXTURES_PATH = os.path.join(os.getcwd(), 'fixtures')


def _populate_table_with_json(table, filename: str):
    with open(os.path.join(FIXTURES_PATH, filename)) as file:
        for item in json.load(file):
            table.add(**item)


class Database:

    @staticmethod
    def recreate_db():
        db.drop_all()
        db.create_all()

        _populate_table_with_json(Category, 'category.json')
        _populate_table_with_json(Skin, 'skin.json')

    @staticmethod
    def get_categories():
        return Category.query.all()

    @staticmethod
    def get_skins_by_category(category_name: str):
        category_id = Category.query.filter_by(name=category_name).first()
        return Skin.query.filter_by(category=category_id).all()

    def get_user(self):
        pass

    def get_user_skins(self):
        pass

    def add_order(self, data):
        pass

    @staticmethod
    def add_user(data):
        User.add(*data)
        # TODO: add free skins

    def add_skin_to_user(self, data):
        pass
