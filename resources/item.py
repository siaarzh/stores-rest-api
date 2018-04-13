import psycopg2
from config import config

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank.'
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "No item by the name '{}' in table 'items'".format(str(name))}, 404

    # add a dict / status code for non-existent
    @jwt_required()
    def post(self, name):
        # Check for existing item before appending
        if ItemModel.find_by_name(name):
            return {'message': "An item with the name '{}' already exists".format(name)}, 400

        # Paste item attributes
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        # Append item to database
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201  # feedback, status code for CREATED

    @jwt_required()
    def delete(self, name):

        delete_query = "DELETE FROM items WHERE name=%s"
        ItemModel.db_query(delete_query, (name,))

        return {'message': "Item '{}' deleted.".format(name)}

    @jwt_required()
    def put(self, name):
        """
        Updates an item or adds it, if it does not exist
        Course section 5: video 72, 73

        :param name: item dictionary
        :return: item json
        """

        data = Item.parser.parse_args()
        # Check for existing item before appending
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500  # internal server error
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500  # internal server error
        return updated_item.json()


# noinspection PyMethodMayBeStatic
class ItemList(Resource):
    def get(self):
        """
        Returns a JSON with all items in database "items" table
        Course section: 5, video 74

        :return: JSON of items
        """
        query = "SELECT * FROM items"
        items = []
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            for row in cursor:
                items.append({"name": row[0], "price": row[1]})
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return {"An error occurred"}, 500

        finally:
            if connection is not None:
                connection.close()

        return {'items': items}
