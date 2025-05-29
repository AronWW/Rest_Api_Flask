from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from models import db
from resources import BookListResource, BookResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/books_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SWAGGER'] = {'title': 'Books API', 'uiversion': 3}

Swagger(app)

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
api.add_resource(BookListResource, '/books/')
api.add_resource(BookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)