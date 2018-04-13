import psycopg2

from config import config
from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
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

        query = "SELECT * FROM users WHERE username=%s"
        return UserModel.db_query(query, (username,))

    @staticmethod
    def find_by_id(_id):

        query = "SELECT * FROM users WHERE user_id=%s"
        return UserModel.db_query(query, (_id,))