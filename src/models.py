from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites_characters: Mapped[list["FavoriteCharacters"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="joined")
    favorites_planets: Mapped[list["FavoritePlanets"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="joined")
    favorites_starships: Mapped[list["FavoriteStarships"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
        return f"Usuario con id {self.id} y email: {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
            "favorite_characters": [fav.serialize() for fav in (self.favorites_characters or [])],
            "favorite_planets": [fav.serialize() for fav in (self.favorites_planets or[])],
            "favorite_starships": [fav.serialize() for fav in (self.favorites_starships or [])]
        }

# -------------------------------


class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_characters_by: Mapped[list["FavoriteCharacters"]] = relationship(
        back_populates="characters", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
       return f"Personaje: {self.name} ; Descripcion: {self.comment_text}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "comment_text": self.comment_text
        } 

class FavoriteCharacters(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_characters")
    characters_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    characters: Mapped["Characters"] = relationship(
        back_populates="favorite_characters_by")
    
    def __repr__(self):
        return f"Id:{self.id} del favorito . {self.user}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            "characters": self.characters.serialize() if self.characters else None,
        }

# ---------------------------------


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=False)
    favorite_planets_by: Mapped[list["FavoritePlanets"]] = relationship(
        back_populates="planets", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
       return f"Planeta: {self.name} ; Descripcion: {self.comment_text}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "comment_text": self.comment_text
        }
    

class FavoritePlanets(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_planets")
    planets_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    planets: Mapped["Planets"] = relationship(
        back_populates="favorite_planets_by")

    def __repr__(self):
        return f"Id:{self.id} del favorito . {self.user}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id,
            "planets": self.planets.serialize() if self.planets else None,
        }

# -------------------------

class Starships(db.Model):
    __tablename__ = "starships"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    comment_text: Mapped[str] = mapped_column(String(120), nullable=True)
    favorite_starships_by: Mapped[list["FavoriteStarships"]] = relationship(
        back_populates="starships", cascade="all, delete-orphan", lazy="joined")

    def __repr__(self):
       return f"Nave de Batalla: {self.name} ; Descripcion: {self.comment_text}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "comment_text": self.comment_text
        }

class FavoriteStarships(db.Model):
   
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="favorites_starships")
    starships_id: Mapped[int] = mapped_column(ForeignKey("starships.id"))
    starships: Mapped["Starships"] = relationship(
        back_populates="favorite_starships_by")

    def __repr__(self):
        return f"Id:{self.id} del favorito . {self.user}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starships_id": self.starships_id,
            "starship": self.starships.serialize() if self.starships else None
        }