"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, CharacterFavorite, PlanetFavorite

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():

    request_body_user = request.get_json()
    user1 = User(
        first_name=request_body_user["first_name"],
        email=request_body_user["email"], 
        password=request_body_user["password"]
        )
    db.session.add(user1)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def modify_user(user_id):

    request_body_user = request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User noooot found', status_code=404)
    if "username" in request_body_user:
        user1.username = body["username"]
    if "email" in request_body_user:
        user1.email = body["email"]
    if "first_name" in request_body_user:
        user1.first_name = request_body_user["first_name"]
    db.session.commit()
    return jsonify(request_body_user), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    request_body_user = request.get_json()
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify(request_body_user), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):

        request_body_character = request.get_json()
        character1 = Character.query.get(character_id)
        return jsonify(character1.serialize()), 200


@app.route('/character', methods=['GET'])
def get_characters():

    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_characters), 200


@app.route('/character', methods=['POST'])
def add_character():

    request_body_character = request.get_json()
    character1 = Character(
    name=request_body_character["name"],
    birth_year=request_body_character["birth_year"]
    )
    db.session.add(character1)
    db.session.commit()
    return jsonify(request_body_character), 200

@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):

    request_body_character = request.get_json()
    character1 = Character.query.get(character_id)
    if character1 is None:
        raise APIException('Character not found', status_code=404)
    db.session.delete(character1)
    db.session.commit()
    return jsonify(request_body_character), 200

@app.route('/planet', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    request_body_planet = request.get_json()
    planet1 = Planet.query.get(planet_id)
    return jsonify(planet1.serialize()), 200

@app.route('/planet', methods=['POST'])
def add_planet():

    request_body_planet = request.get_json()
    planet1 = Planet(
    name=request_body_planet["name"],
    climate=request_body_planet["climate"]
    )
    db.session.add(planet1)
    db.session.commit()
    return jsonify(request_body_planet), 200

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['GET', 'POST'])
def fav_characters(user_id, character_id):
    
    if request.method=='POST':
        request_body_character = request.get_json()
        character1 = Character.query.get(character_id)
        new_favorite= CharacterFavorite(user_id=user_id, character_id=character_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(request_body_character), 200
    else: 
        favorites=CharacterFavorite.query.filter_by(user_id=user_id).all()
        all_characters = list(map(lambda x: x.serialize(), favorites))
        return jsonify(all_characters), 200


@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_fav_character(user_id, character_id):

        request_body_character = request.get_json()
        character1 = Character.query.get(character_id)
        if character1 is None:
            raise APIException('Character not found', status_code=404)
        db.session.delete(character1)
        db.session.commit()
        return jsonify(request_body_character), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['GET', 'POST'])
def fav_planets(user_id, planet_id):
    
    if request.method=='POST':
        request_body_planet = request.get_json()
        planet1 = Planet.query.get(planet_id)
        new_favorite= PlanetFavorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(request_body_planet), 200
    else: 
        favoritesp=PlanetFavorite.query.filter_by(user_id=user_id).all()
        all_planets = list(map(lambda x: x.serialize(), favoritesp))
        return jsonify(all_planets), 200

@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(user_id, character_id):

        request_body_planet = request.get_json()
        planet1 = Planet.query.get(planet_id)
        if planet1 is None:
            raise APIException('Planet not found', status_code=404)
        db.session.delete(planet1)
        db.session.commit()
        return jsonify(request_body_planet), 200








# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)