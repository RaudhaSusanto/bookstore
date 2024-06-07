from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from resources.book import BookResources
from resources.user import UserResources
from resources.category import CategoryResources
from resources.publisher import PublisherResources
from resources.author import AuthorResources

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Bookstore API!"

if __name__ == '__main__':
    app.run(debug=True)

api = Api(app)
api.add_resource(BookResources, '/books')
api.add_resource(UserResources, '/users')
api.add_resource(CategoryResources, '/categories')
api.add_resource(PublisherResources, '/publishers')
api.add_resource(AuthorResources, '/authors')

from models import Book, Author, Category, Publisher

def build_sql_query(model, params):
    query = model.query

    if 'title' in params and hasattr(model, 'title'):
        query = query.filter(model.title.ilike(f"%{params['title']}%"))
    if 'name' in params and hasattr(model, 'name'):
        query = query.filter(model.name.ilike(f"%{params['name']}%"))
    if 'price_min' in params and hasattr(model, 'price'):
        query = query.filter(model.price >= params['price_min'])
    if 'price_max' in params and hasattr(model, 'price'):
        query = query.filter(model.price <= params['price_max'])
    if 'author' in params and model == Book:
        query = query.join(Author).filter(Author.name.ilike(f"%{params['author']}%"))
    if 'category' in params and model == Book:
        query = query.join(Category).filter(Category.name.ilike(f"%{params['category']}%"))
    if 'publisher' in params and model == Book:
        query = query.join(Publisher).filter(Publisher.name.ilike(f"%{params['publisher']}%"))

    return query.all()

@app.route('/search', methods=['GET'])
def search_books():
    params = request.args.to_dict()
    books = build_sql_query(Book, params)
    return jsonify([book.serialize() for book in books])

def perform_transaction(operations):
    try:
        for operation in operations:
            db.session.add(operation)
        db.session.commit()
        return {"message": "Transaction completed successfully"}
    except Exception as e:
        db.session.rollback()
        return {"message": f"Transaction failed: {str(e)}"}, 500
