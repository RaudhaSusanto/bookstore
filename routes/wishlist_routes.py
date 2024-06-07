
from flask import Blueprint, request, jsonify
from models import db, User_Wishlist, Wishlist_Items
from sqlalchemy.exc import SQLAlchemyError

wishlist_blueprint = Blueprint('wishlists', __name__)

@wishlist_blueprint.route('/wishlists/<int:user_id>', methods=['POST'])
def add_to_wishlist(user_id):
    try:
        book_id = request.json.get('book_id')
        user_wishlist = User_Wishlist.query.filter_by(user_id=user_id).first()

        if not user_wishlist:
            user_wishlist = User_Wishlist(user_id=user_id)
            db.session.add(user_wishlist)
            db.session.commit()

        wishlist_item = Wishlist_Items(wishlist_id=user_wishlist.wishlist_id, book_id=book_id)
        db.session.add(wishlist_item)
        db.session.commit()

        return jsonify({'message': 'Buku ditambahkan ke wishlist'}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
