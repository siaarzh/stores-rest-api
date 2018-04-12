import psycopg2
from config import config

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):


	parser = reqparse.RequestParser()
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help='This field cannot be left blank.'
	)

	@classmethod
	def db_query(cls, query, query_args): # not using self in the method, but using class name

		connection = None
		try:
			params = config()
			connection = psycopg2.connect(**params)
			cursor = connection.cursor()
			cursor.execute(query, query_args) # make sure query_args is a tuple, e.g.: (item,)
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

	def get(self, name):
		query = "SELECT * FROM items WHERE name=%s"
		data = self.db_query(query, (name,))
		if data:
			return {'item': {'name': data[0], 'price': data[1]}}
		return {'message': "No item by the name '{}' in table 'items'".format(str(name))}, 404

	# add a dict / status code for non-existent
	@jwt_required()
	def post(self, name):
		# Check for existing item before appending
		query = "SELECT * FROM items WHERE name=%s"
		if self.db_query(query, (name,)):
			return {'message': "An item with the name '{}' already exists".format(name)}, 400

		# Paste item attributes
		data = Item.parser.parse_args()
		item = {'name': name, 'price': data['price']}

		# Append item to database
		append_query = "INSERT INTO items (name, price) VALUES (%(name)s, %(price)s)"
		try:
			self.db_query(append_query, item)
		except:
			return {"message": "An error occurred inserting the item."}, 500 # internal server error

		return item, 201  # feedback, status code for CREATED

	@jwt_required()
	def delete(self, name):

		delete_query = "DELETE FROM items WHERE name=%s"
		self.db_query(delete_query, (name,))

		# global items
		# if next(filter(lambda x: x['name'] == name, items), None) is None:
		# 	return {'message': "An item with the name '{}' does not exist".format(name)}, 400
		# items = list(filter(lambda x: x['name'] != name, items))
		return {'message': "Item '{}' deleted.".format(name)}

	@jwt_required()
	def put(self, name):
		'''
		Updates an item or adds it, if it does not exist
		Course section 5: video 72, 73

		:param name: item dictionary
		:return: item json
		'''

		data = Item.parser.parse_args()
		# Check for existing item before appending
		query = "SELECT * FROM items WHERE name=%s"
		item = self.db_query(query, (name,))
		updated_item = {"name": name, "price": data["price"]}

		if item is None:
			append_query = "INSERT INTO items (name, price) VALUES (%(name)s, %(price)s)"
			try:
				self.db_query(append_query, updated_item)
			except:
				return {"message": "An error occurred inserting the item."}, 500  # internal server error
		else:
			update_query = "UPDATE items SET price=%(price)s WHERE name=%(name)s"
			try:
				self.db_query(update_query, updated_item)
			except:
				return {"message": "An error occurred updating the item."}, 500  # internal server error
		return updated_item


class ItemList(Resource):
	def get(self):
		return {'items': items}