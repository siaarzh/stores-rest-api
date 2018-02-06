from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'randomword'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True) # <--- FOR RUNNING ON LOCAL MACHINE
# app.run(host='0.0.0.0', port=5000) # <--- FOR RUNNING ON LAN (Remember to open port)
