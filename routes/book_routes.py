
from flask import Blueprint, request, jsonify
from models import db, Book
from utils.sql_builder import build_sql_query

book_blueprint = Blueprint('books', __name__)

@book_blueprint.route('/books', methods=['GET'])
def get_books():
    params = request.args.to_dict()
    books = build_sql_query(params)
    return jsonify([book.to_dict() for book in books])

@book_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())

@book_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = Book.query.get_or_404(book_id)

    if 'price' in data:
        book.price = data['price']
    if 'description' in data:
        book.description = data['description']

    db.session.commit()
    return jsonify(book.to_dict())
