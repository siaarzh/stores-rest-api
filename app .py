from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'randomword'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):


	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help='This field cannot be left blank.'
	)

	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item else 404  # other apps may not accept python's None, therefor we need to

	# add a dict / status code for non-existent
	@jwt_required()
	def post(self, name):
		# load data only after we check for existing entry
		if next(filter(lambda x: x['name'] == name, items), None) is not None:
			return {'message': "An item with the name '{}' already exists".format(name)}, 400

		data = Item.parser.parse_args()

		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201  # feedback, status code for CREATED

	@jwt_required()
	def delete(self, name):
		global items
		if next(filter(lambda x: x['name'] == name, items), None) is None:
			return {'message': "An item with the name '{}' does not exist".format(name)}, 400
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': "Item '{}' deleted.".format(name)}

	@jwt_required()
	def put(self, name):

		data = Item.parser.parse_args()

		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item


class ItemList(Resource):
	def get(self):
		return {'items': items}


api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True) # <--- FOR RUNNING ON LOCAL MACHINE
# app.run(host='0.0.0.0', port=5000) # <--- FOR RUNNING ON LAN (Remember to open port)
