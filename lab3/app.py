from flask import Flask
from models import db
from routes import book_bp
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://postgres:postgres@db:5432/library'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(book_bp, url_prefix="/books")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)