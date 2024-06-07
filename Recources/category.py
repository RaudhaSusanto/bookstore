from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import Category, db

app = Flask(__name__)
api = Api(app)

class CategoryResource(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return {"message": "Category not found"}, 404
            return jsonify(category.serialize())
        else:
            categories = Category.query.all()
            return jsonify([category.serialize() for category in categories])

    def post(self):
        data = request.json
        new_category = Category(name=data['name'], description=data.get('description'))
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.serialize())

    def put(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {"message": "Category not found"}, 404
        data = request.json
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        db.session.commit()
        return jsonify(category.serialize())

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            return {"message": "Category not found"}, 404
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted successfully"}
        
api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')
        
if __name__ == '__main__':
    app.run(debug=True)