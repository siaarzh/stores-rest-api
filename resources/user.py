import psycopg2
from config import config
from flask_restful import Resource, reqparse

from models.user import UserModel

'''
UPDATED: TO USE POSTGRESQL TO STORE USER CREDENTIALS
'''


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
        if UserModel.find_by_username(data['username']):
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
