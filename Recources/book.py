from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import Book, db

app = Flask(__name__)
api = Api(app)

class BookResource(Resource):
    def get(self, book_id=None):
        if book_id:
            book = Book.query.get(book_id)
            if not book:
                return {"message": "Book not found"}, 404
            return jsonify(book.serialize())
        else:
            books = Book.query.all()
            return jsonify([book.serialize() for book in books])

    def post(self):
        data = request.json
        new_book = Book(title=data['title'], author_id=data['author_id'], publisher_id=data['publisher_id'], category_id=data['category_id'],
                        isbn=data['isbn'], publication_year=data['publication_year'], price=data['price'],
                        description=data['description'], cover_image=data['cover_image'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.serialize())

    def put(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        data = request.json
        book.title = data.get('title', book.title)
        book.author_id = data.get('author_id', book.author_id)
        book.publisher_id = data.get('publisher_id', book.publisher_id)
        book.category_id = data.get('category_id', book.category_id)
        book.isbn = data.get('isbn', book.isbn)
        book.publication_year = data.get('publication_year', book.publication_year)
        book.price = data.get('price', book.price)
        book.description = data.get('description', book.description)
        book.cover_image = data.get('cover_image', book.cover_image)
        db.session.commit()
        return jsonify(book.serialize())

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted successfully"}
        
api.add_resource(BookResource, '/books', '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)