from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.Int(dump_only=True, description="The book's unique identifier")
    title = fields.Str(required=True, validate=validate.Length(min=1), description="The book's title")
    author = fields.Str(required=True, validate=validate.Length(min=1), description="The book's author")
    year = fields.Int(required=True, validate=validate.Range(min=0), description="The book's publication year")

book_schema = BookSchema()
books_schema = BookSchema(many=True)