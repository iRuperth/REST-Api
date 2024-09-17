import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL") 
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("https://swapi.dev/api", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///your_local_database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    try:
        people = Character.query.all()
        people_list = [p.to_dict() for p in people]
        return jsonify(people_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    try:
        person = Character.query.get(people_id)
        if not person:
            return jsonify({"message": "Character not found"}), 404
        return jsonify(person.to_dict()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets = Planet.query.all()
        planet_list = [p.to_dict() for p in planets]
        return jsonify(planet_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"message": "Planet not found"}), 404
        return jsonify(planet.to_dict()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        user_list = [u.to_dict() for u in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    try:
        user = User.query.get(1)
        if not user:
            return jsonify({"message": "User not found"}), 404
        favorite_list = [f.to_dict() for f in user.favorites]
        return jsonify(favorite_list), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        user = User.query.get(1)  
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"message": "Planet not found"}), 404
        favorite = Favorite(user_id=user.id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"message": "Planet added to favorites"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    try:
        user = User.query.get(1) 
        person = Character.query.get(people_id)
        if not person:
            return jsonify({"message": "Character not found"}), 404
        favorite = Favorite(user_id=user.id, character_id=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"message": "Character added to favorites"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    try:
        user = User.query.get(1) 
        favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
        if not favorite:
            return jsonify({"message": "Favorite not found"}), 404
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite planet removed"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_person(people_id):
    try:
        user = User.query.get(1)  
        favorite = Favorite.query.filter_by(user_id=user.id, character_id=people_id).first()
        if not favorite:
            return jsonify({"message": "Favorite not found"}), 404
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite character removed"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)