from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import Publisher, db

app = Flask(__name__)
api = Api(app)

class PublisherResource(Resource):
    def get(self, publisher_id=None):
        if publisher_id:
            publisher = Publisher.query.get(publisher_id)
            if not publisher:
                return {"message": "Publisher not found"}, 404
            return jsonify(publisher.serialize())
        else:
            publishers = Publisher.query.all()
            return jsonify([publisher.serialize() for publisher in publishers])

    def post(self):
        data = request.json
        new_publisher = Publisher(name=data['name'], address=data.get('address'), website=data.get('website'))
        db.session.add(new_publisher)
        db.session.commit()
        return jsonify(new_publisher.serialize())

    def put(self, publisher_id):
        publisher = Publisher.query.get(publisher_id)
        if not publisher:
            return {"message": "Publisher not found"}, 404
        data = request.json
        publisher.name = data.get('name', publisher.name)
        publisher.address = data.get('address', publisher.address)
        publisher.website = data.get('website', publisher.website)
        db.session.commit()
        return jsonify(publisher.serialize())

    def delete(self, publisher_id):
        publisher = Publisher.query.get(publisher_id)
        if not publisher:
            return {"message": "Publisher not found"}, 404
        db.session.delete(publisher)
        db.session.commit()
        return {"message": "Publisher deleted successfully"}
        
api.add_resource(PublisherResource, '/publishers', '/publishers/<int:publisher_id>')

if __name__ == '__main__':
    app.run(debug=True)