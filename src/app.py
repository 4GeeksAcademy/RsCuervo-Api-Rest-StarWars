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
from sqlalchemy.orm import joinedload
from models import db, User, Characters, FavoriteCharacters, Planets, FavoritePlanets, Starships, FavoriteStarships
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
    users = User.query.options(
        joinedload(User.favorites_characters),
        joinedload(User.favorites_planets),
        joinedload(User.favorites_starships)
    ).all()
    print(users)

    # users_serialized = []
    # for user in users:
    #   users_serialized.append(user.serialize())
    # --------------------------------------
    users_serialized = list(map(lambda user: user.serialize(), users))
    # -------------------------------------
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "users": users_serialized
    }

    return jsonify(response_body), 200

# -----GET de todos los personajes---


@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    response = [person.serialize() for person in characters]
    return jsonify(response), 200

# ---- GET de cada personaje por su id---


@app.route('/character/<int:character_id>', methods=['GET'])
def get_character_by_id(characters_id):
    person = Characters.query.get(characters_id)
    if not person:
        return jsonify({'msg': 'Personaje no encontrado'})
    return jsonify(person.serialize()), 200

# ----GET de Planetas----


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    response = [planet.serialize() for planet in planets]
    return jsonify(response), 200

# -----GET de un Planeta por su Id----


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planets_id):
    planet = Planets.query.get(planets_id)
    if not planet:
        return jsonify({"message": "Planet no encontrado"}), 404
    return jsonify(planet.serialize()), 200

# ----GET de Starships---


@app.route('/starships', methods=['GET'])
def get_starships():
    starships = Starships.query.all()
    response = [starship.serialize() for starship in starships]
    return jsonify(response), 200

# --- GET de Starship por su ID


@app.route('/starships/<int:starship_id>', methods=['GET'])
def get_starship_by_id(starships_id):
    starship = Starships.query.get(starships_id)
    if not starship:
        return jsonify({"message": "Starship not found"}), 404
    return jsonify(starship.serialize()), 200

# ----GET de Todos los favoritos del usuario


@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"msg": "User ID es requirido"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    favorites = {
        "favorite_characters": [fav.serialize() for fav in user.favorites_characters],
        "favorite_planets": [fav.serialize() for fav in user.favorites_planets],
        "favorite_starships": [fav.serialize() for fav in user.favorites_starships]
    }
    return jsonify(favorites), 200

# ----------[POST] anadir un planeta favorito


@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):
    body = request.get_json()
    user_id = body.get("user_id")
    if not user_id:
        return jsonify({'msg': 'El campo "user_id" es obligatorio'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    favorite = FavoritePlanets(user_id=user_id, planets_id=planets_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Planeta añadido a favoritos exitosamente'}), 201

# --------[POST] anadir un personaje Favorito


@app.route('/favorite/characters/<int:characters_id>', methods=['POST'])
def add_favorite_character(characters_id):
    body = request.get_json()
    user_id = body.get("user_id")
    if not user_id:
        return jsonify({'msg': 'El campo "user_id" es obligatorio'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    favorite = FavoriteCharacters(user_id=user_id, characters_id=characters_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Personaje añadido a favoritos exitosamente'}), 201

# ------[POST] anadir una nave espacial favorita


@app.route('/favorite/starships/<int:starships_id>', methods=['POST'])
def add_favorite_starship(starships_id):
    body = request.get_json()
    user_id = body.get("user_id")
    if not user_id:
        return jsonify({'msg': 'El campo "user_id" es obligatorio'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    favorite = FavoriteStarships(user_id=user_id, starships_id=starships_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Nave espacial añadida a favoritos exitosamente'}), 201

# ------[DELETE]


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    body = request.get_json()
    user_id = body.get("user_id")
    if not user_id:
        return jsonify({'msg': 'El campo "user_id" es obligatorio'}), 400

    favorite = FavoritePlanets.query.filter_by(
        user_id=user_id, planets_id=planet_id).first()
    if not favorite:
        return jsonify({'msg': 'Favorito no encontrado'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Planeta eliminado de favoritos exitosamente'}), 200


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    body = request.get_json()
    user_id = body.get("user_id")
    if not user_id:
        return jsonify({'msg': 'El campo "user_id" es obligatorio'}), 400

    favorite = FavoriteCharacters.query.filter_by(
        user_id=user_id, characters_id=character_id).first()
    if not favorite:
        return jsonify({'msg': 'Favorito no encontrado'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Personaje eliminado de favoritos exitosamente'}), 200


@app.route('/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(starship_id):
    body = request.get_json()
    user_id = body.get("user_id")
    if not user_id:
        return jsonify({'msg': 'El campo "user_id" es obligatorio'}), 400

    favorite = FavoriteStarships.query.filter_by(
        user_id=user_id, starships_id=starship_id).first()
    if not favorite:
        return jsonify({'msg': 'Favorito no encontrado'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Nave espacial eliminada de favoritos exitosamente'}), 200

# -------------------------------


@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Debes enviar informacion en el body'})
    if 'email' not in body:
        return jsonify({'msg': 'El campo "email" es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'El campo "password" es obligatorio'}), 400

    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True

    return jsonify({'msg': 'ok'})


'''
@app.route('/get-favorites', methods=['GET'])
def get_favorites():
    user = User.query.get()
    print(user.favorite_characters)
    print(user.favorite_planets)
    print(user.favorite_starships)
    return jsonify({'msg': 'ok'})
'''


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
