from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'randomword'
api = Api(app)
# app.config['JWT_AUTH_URL_RULE'] = '/login' # authentication endpoint as per lecture 75

jwt = JWT(app, authenticate, identity)  # /auth

# # config JWT to expire within half an hour (lec 75)
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
#
# # config JWT auth key name to be 'email' instead of default 'username' (lec 75)
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # <--- FOR RUNNING ON LOCAL MACHINE
    # app.run(host='0.0.0.0', port=5000) # <--- FOR RUNNING ON LAN (Remember to open port)
