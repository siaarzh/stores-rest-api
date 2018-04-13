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
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500  # internal server error

        return item.json(), 201  # feedback, status code for CREATED

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item '{}' deleted.".format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Check for existing item before appending
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

