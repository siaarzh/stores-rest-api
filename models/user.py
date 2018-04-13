import psycopg2

from config import config
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def db_query(cls, query, query_args):  # not using self in the method, but using class name

        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()

            cursor.execute(query, query_args)  # make sure query_args is a tuple, e.g.: (item,)
            row = cursor.fetchone()

            if row:
                result = cls(*row)  # *row gets expanded automatically
            else:
                result = None
            # close the communication with the PostgreSQL
            cursor.close()
            return result

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if connection is not None:
                connection.close()
                # print('Database connection closed.')

    @staticmethod
    def find_by_username(username):
        return UserModel.query.filter_by(username=username).first()

    @staticmethod
    def find_by_id(_id):
        return UserModel.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
