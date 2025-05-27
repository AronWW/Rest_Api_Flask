from flask import Flask
from routes import book_bp

app = Flask(__name__)
app.register_blueprint(book_bp, url_prefix="/books")

if __name__ == "__main__":
    app.run(debug=True)
