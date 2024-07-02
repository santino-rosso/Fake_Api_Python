from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import RatingModel

class Rating(Resource):
    def get(self,id):
        rating=db.session.query(RatingModel).get_or_404(id)
        return rating.to_json()

    def delete(self,id):
        rating=db.session.query(RatingModel).get_or_404(id)
        db.session.delete(rating)
        db.session.commit()
        return "", 204
        
    def put(self,id):
        rating=db.session.query(RatingModel).get_or_404(id)
        data=request.get_json().items()
        for key, value in data:
            setattr(rating, key, value)
        db.session.add(rating)
        db.session.commit()
        return rating.to_json(), 201
    

class Ratings(Resource):
        def get(self):
            ratings=db.session.query(RatingModel)
            return jsonify([rating.to_json() for rating in ratings])
            
        def post(self):
            ratings = RatingModel.from_json(request.get_json())
            print(ratings)
            try:
                db.session.add(ratings)
                db.session.commit()
            except:
                return 'Formato no correcto', 400
            return ratings.to_json(), 201