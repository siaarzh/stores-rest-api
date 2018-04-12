import psycopg2
from config import config
from flask_restful import Resource, reqparse

'''
UPDATED: TO USE POSTGRESQL TO STORE USER CREDENTIALS
'''


class User:
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
        return User.db_query(query, (username,))

    @staticmethod
    def find_by_id(_id):

        query = "SELECT * FROM users WHERE user_id=%s"
        return User.db_query(query, (_id,))


# noinspection PyMethodMayBeStatic
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be left blank.'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be left blank.'
    )

    def post(self):

        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "User '{}' already exits.".format(data['username'])}, 400

        connection = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()

            query = "INSERT INTO users VALUES (DEFAULT, %s, %s)"
            cursor.execute(query, (data['username'], data['password']))

            # close the communication with the PostgreSQL
            cursor.close()
            return {"message": "User '{}' created successfully.".format(data['username'])}, 201

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if connection is not None:
                connection.commit()  # always commit when using INSERT to save the data on database
                connection.close()
                print('Database connection closed.')
