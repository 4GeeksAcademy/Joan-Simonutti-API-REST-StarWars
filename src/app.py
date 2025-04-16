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
from models import db, Users, Peoples, Planets, Species, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

@app.route('/people', methods=['GET'])
def get_people():
    people = Peoples.query.all()
    return jsonify([person.serialize() for person in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Peoples.query.get_or_404(people_id)
    return jsonify(person.serialize())

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
    person = Peoples.query.get_or_404(people_id)
    data = request.json
    
    if 'name' in data:
        person.name = data['name']
    if 'gender' in data:
        person.gender = data['gender']
    if 'hair_color' in data:
        person.hair_color = data['hair_color']
    
    db.session.commit()
    return jsonify({'message': 'People updated successfully', 'people': person.serialize()})

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    person = Peoples.query.get_or_404(people_id)
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'People deleted successfully'})

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    return jsonify(planet.serialize())

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    data = request.json
    
    if 'name' in data:
        planet.name = data['name']
    if 'terrain' in data:
        planet.terrain = data['terrain']
    if 'climate' in data:
        planet.climate = data['climate']
    if 'rotation_period' in data:
        planet.rotation_period = data['rotation_period']
    
    db.session.commit()
    return jsonify({'message': 'Planet updated successfully', 'planet': planet.serialize()})

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({'message': 'Planet deleted successfully'})

@app.route('/species', methods=['GET'])
def get_species():
    species = Species.query.all()
    return jsonify([specie.serialize() for specie in species])

@app.route('/species/<int:species_id>', methods=['GET'])
def get_single_species(species_id):
    specie = Species.query.get_or_404(species_id)
    return jsonify(specie.serialize())

@app.route('/species/<int:species_id>', methods=['PUT'])
def update_species(species_id):
    specie = Species.query.get_or_404(species_id)
    data = request.json
    
    if 'name' in data:
        specie.name = data['name']
    if 'average_height' in data:
        specie.average_height = data['average_height']
    if 'hair_colors' in data:
        specie.hair_colors = data['hair_colors']
    if 'skin_colors' in data:
        specie.skin_colors = data['skin_colors']
    
    db.session.commit()
    return jsonify({'message': 'Species updated successfully', 'species': specie.serialize()})

@app.route('/species/<int:species_id>', methods=['DELETE'])
def delete_species(species_id):
    specie = Species.query.get_or_404(species_id)
    db.session.delete(specie)
    db.session.commit()
    return jsonify({'message': 'Species deleted successfully'})

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.serialize() for user in users])

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    favorites = Favorites.query.filter_by(users_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites])

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
