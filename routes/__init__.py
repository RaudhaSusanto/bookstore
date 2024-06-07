
from .book_routes import book_blueprint
from .wishlist_routes import wishlist_blueprint

def register_routes(app):
    app.register_blueprint(book_blueprint)
    app.register_blueprint(wishlist_blueprint)
