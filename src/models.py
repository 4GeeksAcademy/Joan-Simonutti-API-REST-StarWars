from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('peoples.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=True)
    user = db.relationship('Users', backref='favorites')  
    people = db.relationship('Peoples', backref='favorites')  
    planet = db.relationship('Planets', backref='favorites')  
    species = db.relationship('Species', backref='favorites')  

    def serialize(self):
        return {
            "id": self.id,
            "users_id": self.users_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id,
            "species_id": self.species_id,
            "people": self.people.serialize() if self.people else None,
            "planet": self.planet.serialize() if self.planet else None,
            "species": self.species.serialize() if self.species else None
        }


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # No serializar la contraseña por seguridad
        }


class Peoples(db.Model):
    __tablename__ = 'peoples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    hair_color = db.Column(db.String(80), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='peoples')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "users_id": self.users_id
        }


class Planets(db.Model):
    __tablename__ = 'planets'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    terrain = db.Column(db.String(80), nullable=False)
    climate = db.Column(db.String(80), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='planets')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "users_id": self.users_id
        }


class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    average_height = db.Column(db.Integer, nullable=False)
    hair_colors = db.Column(db.String(80), nullable=False)
    skin_colors = db.Column(db.String(80), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='species')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "average_height": self.average_height,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,
            "users_id": self.users_id
        }