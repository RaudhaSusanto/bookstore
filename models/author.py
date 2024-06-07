from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import Author, db

app = Flask(__name__)
api = Api(app)

class AuthorResource(Resource):
    def get(self, author_id=None):
        if author_id:
            author = Author.query.get(author_id)
            if not author:
                return {"message": "Author not found"}, 404
            return jsonify(author.serialize())
        else:
            authors = Author.query.all()
            return jsonify([author.serialize() for author in authors])

    def post(self):
        data = request.json
        new_author = Author(name=data['name'], biography=data.get('biography'), date_of_birth=data.get('date_of_birth'))
        db.session.add(new_author)
        db.session.commit()
        return jsonify(new_author.serialize())

    def put(self, author_id):
        author = Author.query.get(author_id)
        if not author:
            return {"message": "Author not found"}, 404
        data = request.json
        author.name = data.get('name', author.name)
        author.biography = data.get('biography', author.biography)
        author.date_of_birth = data.get('date_of_birth', author.date_of_birth)
        db.session.commit()
        return jsonify(author.serialize())

    def delete(self, author_id):
        author = Author.query.get(author_id)
        if not author:
            return {"message": "Author not found"}, 404
        db.session.delete(author)
        db.session.commit()
        return {"message": "Author deleted successfully"}
        
        
 api.add_resource(AuthorResource, '/authors', '/authors/<int:author_id>')       
        
if __name__ == '__main__':
    app.run(debug=True)