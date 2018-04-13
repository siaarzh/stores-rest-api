import psycopg2

from config import config


class ItemModel():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @staticmethod
    def db_query(query, query_args):  # not using self in the method, but using class name

        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(query, query_args)  # make sure query_args is a tuple, e.g.: (item,)
            connection.commit()
            row = cursor.fetchone()

            if row:
                return row
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

    @classmethod
    def find_by_name(cls, name):
        query = "SELECT * FROM items WHERE name=%s"
        data = cls.db_query(query, (name,))
        if data:
            return cls(*data) # returns an ItemModel object with *data as it's variables

    def update(self):
        update_query = "UPDATE items SET price=%(price)s WHERE name=%(name)s"
        self.db_query(update_query, (self.name, self.price))

    def insert(self):
        insert_query = "INSERT INTO items (name, price) VALUES (%(name)s, %(price)s)"
        self.db_query(insert_query, (self.name, self.price))

