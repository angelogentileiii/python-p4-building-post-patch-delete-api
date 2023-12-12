#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Index for Game/Review/User API"

@app.get('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

@app.get('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.get('/reviews')
def reviews():

    reviews = []
    for review in Review.query.all():
        review_dict = review.to_dict()
        reviews.append(review_dict)

    response = make_response(
        reviews,
        200
    )

    return response

@app.get('/reviews/<int:id>')
def review_by_id(id):
    review = Review.query.filter(Review.id == id).first()
    
    if not review:
        return {'Error': f'Review with id {id} does not currently exist.'}, 404

    review_dict = review.to_dict()

    response = make_response(
        review_dict,
        200
    )

    return response

@app.post('/reviews')
def add_review():
    new_review = Review()
    review_data = request.get_json()

    for key in review_data:
        setattr(new_review, key, review_data[key])
    
    db.session.add(new_review)
    db.session.commit()

    return new_review.to_dict(), 201

@app.patch('/reviews/<int:id>')
def update_reviews(id: int):
    review = Review.query.get(id)
    review_data = request.get_json()
    
    if not review:
        return {'Error': f'Review with id {id} does not currently exist.'}
    
    for key in review_data:
        setattr(review, key, review_data[key])

    db.session.add(review)
    db.session.commit()

    return review.to_dict(), 202

@app.delete('/reviews/<int:id>')
def delete_review(id: int):
    review = Review.query.get(id)

    if not review:
        return {'Error': f'Review with id {id} does not currently exist.'}, 404

    db.session.delete(review)
    db.session.commit()
    return {}, 205

@app.get('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
