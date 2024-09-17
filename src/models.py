from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model): 
    __tablename__ = 'user'   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    contrasenia = Column(String(250), nullable=False)
    fecha_suscrip = Column(DateTime, nullable=False, default=datetime.utcnow)
    favorites = relationship('Favorite', back_populates='user')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "apellido": self.apellido,
            "email": self.email,
            "contrasenia": self.contrasenia,
            "fecha_suscrip": self.fecha_suscrip.isoformat()
        }

class Character(db.Model): 
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):  
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Vehicle(db.Model):  
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):  
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='favorites')
    
    character_id = Column(Integer, ForeignKey('character.id'))
    character = relationship('Character')
    
    planet_id = Column(Integer, ForeignKey('planet.id'))
    planet = relationship('Planet')
    
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'))
    vehicle = relationship('Vehicle')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "character_id": self.character_id,
            "character_name": self.character.name if self.character else None,
            "planet_id": self.planet_id,
            "planet_name": self.planet.name if self.planet else None,
            "vehicle_id": self.vehicle_id,
            "vehicle_name": self.vehicle.name if self.vehicle else None,
        }
